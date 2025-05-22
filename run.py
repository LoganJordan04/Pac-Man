import pygame
from pygame.locals import *
from constants import *
from pacman import Pacman
from nodes import NodeGroup
from pellets import PelletGroup
from ghosts import GhostGroup


# Main game controller class: handles setup, input, updates, and rendering
class GameController(object):
    def __init__(self):
        pygame.init()

        # Create the main display surface using screen size defined in constants.py
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)

        # Surface used as the static background (e.g., maze backdrop)
        self.background = None

        # Clock to manage time between frames and limit frame rate
        self.clock = pygame.time.Clock()

    # Creates a plain black background surface.
    # WILL BE REPLACED LATER
    def set_background(self):
        self.background = pygame.surface.Surface(SCREENSIZE).convert()
        self.background.fill(BLACK)

    # Called once at game start. Initializes maze, Pac-Man, ghosts, and pellets.
    # Loads the maze from file, places all entities, and sets up portals and ghost house.
    def start_game(self):
        self.set_background()

        # Load maze layout and create graph of nodes
        self.nodes = NodeGroup("maze1.txt")

        # Link left and right edge nodes as teleport portals
        self.nodes.set_portal_pair((0, 17), (27, 17))

        # Create and connect nodes for the ghost house in the maze
        homekey = self.nodes.create_home_nodes(11.5, 14)
        self.nodes.connect_home_nodes(homekey, (12, 14), LEFT)
        self.nodes.connect_home_nodes(homekey, (15, 14), RIGHT)

        # Initialize Pac-Man at a specific node
        self.pacman = Pacman(self.nodes.get_node_from_tiles(15, 26))

        # Load pellets based on maze layout
        self.pellets = PelletGroup("maze1.txt")

        # Initialize all four ghosts and assign starting positions
        self.ghosts = GhostGroup(self.nodes.get_start_temp_node(), self.pacman)

        self.ghosts.blinky.set_start_node(self.nodes.get_node_from_tiles(2 + 11.5, 0 + 14))
        self.ghosts.pinky.set_start_node(self.nodes.get_node_from_tiles(2 + 11.5, 3 + 14))
        self.ghosts.inky.set_start_node(self.nodes.get_node_from_tiles(0 + 11.5, 3 + 14))
        self.ghosts.clyde.set_start_node(self.nodes.get_node_from_tiles(4 + 11.5, 3 + 14))

        # Set spawn target (ghost house center) for ghosts when eaten
        self.ghosts.set_spawn_node(self.nodes.get_node_from_tiles(2+11.5, 3+14))

    # Runs once per frame. Updates game state, handles events, checks collisions,
    # and draws everything to the screen.
    def update(self):
        # Delta time in seconds (30 FPS)
        dt = self.clock.tick(30) / 1000.0

        # Update entity movement and animation
        self.pacman.update(dt)
        self.ghosts.update(dt)

        # Animate flashing pellets (power pellets)
        self.pellets.update(dt)

        # Handle pellet consumption and score tracking
        self.check_pellet_events()

        # Handle ghost collisions and mode logic
        self.check_ghost_events()

        # Handle user inputs or system quit events
        self.check_events()

        # Draw updated frame to screen
        self.render()

    # Checks for Pygame events such as closing the game window.
    def check_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                # Exit when the user closes the window
                exit()

    # Detect collisions between Pac-Man and ghosts.
    # If a ghost is in freight mode, send it back to the ghost house (spawn mode).
    def check_ghost_events(self):
        for ghost in self.ghosts:
            if self.pacman.collide_ghost(ghost):
                if ghost.mode.current is FREIGHT:
                    ghost.start_spawn()

    # Detects if Pac-Man has eaten a pellet.
    # Removes pellet, increments counter, and triggers ghost freight mode if it's a power pellet.
    def check_pellet_events(self):
        pellet = self.pacman.eat_pellets(self.pellets.pelletList)
        if pellet:
            self.pellets.numEaten += 1
            self.pellets.pelletList.remove(pellet)
            if pellet.name == POWERPELLET:
                self.ghosts.start_freight()

    # Draws all game elements to the screen each frame:
    # background, maze nodes, pellets, Pac-Man, and ghosts.
    def render(self):
        self.screen.blit(self.background, (0, 0))
        self.nodes.render(self.screen)
        self.pellets.render(self.screen)
        self.pacman.render(self.screen)
        self.ghosts.render(self.screen)

        # Refresh the screen with the new frame
        pygame.display.update()


# Entry point for the game: creates and starts the main loop
if __name__ == "__main__":
    game = GameController()
    game.start_game()

    # Main loop runs until manually exited
    while True:
        game.update()
