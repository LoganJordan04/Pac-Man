import pygame
from pygame.locals import *
from constants import *
from pacman import Pacman
from nodes import NodeGroup
from pellets import PelletGroup
from ghosts import Ghost


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

    # Called once at game start to initialize all game components.
    # Loads node graph and portal locations, creates Pac-Man and pellet grid.
    def start_game(self):
        self.set_background()

        # Load maze layout and create graph of nodes
        self.nodes = NodeGroup("maze1.txt")

        # Set portal connections so Pac-Man and ghosts can teleport across the map
        self.nodes.set_portal_pair((0, 17), (27, 17))

        homekey = self.nodes.create_home_nodes(11.5, 14)
        self.nodes.connect_home_nodes(homekey, (12, 14), LEFT)
        self.nodes.connect_home_nodes(homekey, (15, 14), RIGHT)

        # Initialize Pac-Man at a temporary starting node (defined in node group)
        self.pacman = Pacman(self.nodes.get_start_temp_node())

        # Load pellets based on maze layout
        self.pellets = PelletGroup("maze1.txt")

        # Initialize a ghost at the start node, with Pac-Man as its target for AI behavior
        self.ghost = Ghost(self.nodes.get_start_temp_node(), self.pacman)

    # Executes once per frame. Handles game timing, updates, input, and rendering.
    def update(self):
        # Get delta time (in seconds) based on 30 FPS
        dt = self.clock.tick(30) / 1000.0

        # Update entity movement and animation
        self.pacman.update(dt)
        self.ghost.update(dt)

        # Animate and manage pellet flashing (e.g., power pellets)
        self.pellets.update(dt)

        # Handle pellet consumption and score tracking
        self.check_pellet_events()

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

    # Draws all game elements to the screen each frame:
    # background, maze nodes, pellets, Pac-Man, and ghosts.
    def render(self):
        self.screen.blit(self.background, (0, 0))
        self.nodes.render(self.screen)
        self.pellets.render(self.screen)
        self.pacman.render(self.screen)
        self.ghost.render(self.screen)

        # Refresh the screen with the new frame
        pygame.display.update()

    # Checks if Pac-Man has collided with a pellet and handles its removal.
    # Updates the pellet counter.
    def check_pellet_events(self):
        pellet = self.pacman.eat_pellets(self.pellets.pelletList)
        if pellet:
            self.pellets.numEaten += 1
            self.pellets.pelletList.remove(pellet)
            if pellet.name == POWERPELLET:
                self.ghost.start_freight()


# Entry point for the game: creates and starts the main loop
if __name__ == "__main__":
    game = GameController()
    game.start_game()

    # Main loop runs until manually exited
    while True:
        game.update()
