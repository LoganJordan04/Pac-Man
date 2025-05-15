import pygame
from pygame.locals import *
from constants import *
from pacman import Pacman
from nodes import NodeGroup


# Main game controller class: handles setup, input, updates, and rendering
class GameController(object):
    def __init__(self):
        pygame.init()

        # Create the main display surface using screen size defined in constants.py
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)

        # Surface used as the static background (e.g., maze backdrop)
        self.background = None

        # Clock object to manage consistent frame rate and delta timing
        self.clock = pygame.time.Clock()

    # Creates a plain black background surface.
    # WILL BE REPLACED LATER
    def set_background(self):
        self.background = pygame.surface.Surface(SCREENSIZE).convert()
        self.background.fill(BLACK)

    # Initializes all game entities. Called once at launch.
    # Sets up background, maze nodes, portal locations, and places Pac-Man at a starting node.
    def start_game(self):
        self.set_background()
        self.nodes = NodeGroup("maze1.txt")
        self.nodes.set_portal_pair((0, 17), (27, 17))
        self.pacman = Pacman(self.nodes.get_start_temp_node())

    # Executes once per frame. Handles game timing, updates, input, and rendering.
    def update(self):
        # Get delta time (in seconds) based on 30 FPS
        dt = self.clock.tick(30) / 1000.0

        # Update Pac-Man's position
        self.pacman.update(dt)

        # Handle user inputs/events
        self.check_events()

        # Redraw everything
        self.render()

    # Checks for Pygame events such as closing the game window.
    def check_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                # Exit when the user closes the window
                exit()

    # Handles all rendering to the screen: background, characters, etc.
    def render(self):
        # Draw background and pacman
        self.screen.blit(self.background, (0, 0))
        self.nodes.render(self.screen)
        self.pacman.render(self.screen)

        # Push frame to display
        pygame.display.update()


# Entry point for the game: creates and starts the main loop
if __name__ == "__main__":
    game = GameController()
    game.start_game()

    # Main loop runs until manually exited
    while True:
        game.update()
