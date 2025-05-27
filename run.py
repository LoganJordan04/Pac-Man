import pygame
from pygame.locals import *
from constants import *
from pacman import Pacman
from nodes import NodeGroup
from pellets import PelletGroup
from ghosts import GhostGroup
from fruit import Fruit
from pauser import Pause


# Main game controller class: handles setup, updates, input, collisions, and rendering
class GameController(object):
    def __init__(self):
        pygame.init()

        # Create the main display surface using screen size defined in constants.py
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)

        # Surface used as the static background (e.g., maze backdrop)
        self.background = None

        # Clock to manage time between frames and limit frame rate
        self.clock = pygame.time.Clock()

        # Bonus fruit object (appears temporarily)
        self.fruit = None

        # Pause manager for delays and manual pauses
        self.pause = Pause(True)

        # Current level and remaining lives
        self.level = 0
        self.lives = 5

    # Restarts the game from level 0 with full lives after game over.
    def restart_game(self):
        self.lives = 5
        self.level = 0
        self.pause.paused = True
        self.fruit = None
        self.start_game()

    # Resets the current level after a player death (if lives remain).
    def reset_level(self):
        self.pause.paused = True
        self.pacman.reset()
        self.ghosts.reset()
        self.fruit = None

    # Called when all pellets are eaten.
    # Advances to the next level and resets game entities.
    def next_level(self):
        self.show_entities()
        self.level += 1
        self.pause.paused = True
        self.start_game()

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
        self.ghosts.set_spawn_node(self.nodes.get_node_from_tiles(2 + 11.5, 3 + 14))

        # Restrict access to ghost house or junctions as needed
        self.nodes.deny_home_access(self.pacman)
        self.nodes.deny_home_access_list(self.ghosts)
        self.nodes.deny_access_list(2 + 11.5, 3 + 14, LEFT, self.ghosts)
        self.nodes.deny_access_list(2 + 11.5, 3 + 14, RIGHT, self.ghosts)
        self.ghosts.inky.startNode.deny_access(RIGHT, self.ghosts.inky)
        self.ghosts.clyde.startNode.deny_access(LEFT, self.ghosts.clyde)
        self.nodes.deny_access_list(12, 14, UP, self.ghosts)
        self.nodes.deny_access_list(15, 14, UP, self.ghosts)
        self.nodes.deny_access_list(12, 26, UP, self.ghosts)
        self.nodes.deny_access_list(15, 26, UP, self.ghosts)

    # Runs once per frame. Updates game state, handles events, checks collisions,
    # and draws everything to the screen.
    def update(self):
        # Delta time in seconds (30 FPS)
        dt = self.clock.tick(30) / 1000.0

        # Animate flashing pellets (power pellets)
        self.pellets.update(dt)

        if not self.pause.paused:
            # Update entity movement and animation
            self.pacman.update(dt)
            self.ghosts.update(dt)
            if self.fruit is not None:
                self.fruit.update(dt)

            # Handle pellet consumption and score tracking
            self.check_pellet_events()

            # Handle ghost collisions and mode logic
            self.check_ghost_events()

            # Handle fruit consumption and spawning
            self.check_fruit_events()

        afterPauseMethod = self.pause.update(dt)
        if afterPauseMethod is not None:
            afterPauseMethod()

        # Handle user inputs or system quit events
        self.check_events()

        # Draw updated frame to screen
        self.render()

    # Checks for Pygame events such as closing the game window.
    def check_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if self.pacman.alive:
                        self.pause.set_pause(playerPaused=True)
                        if not self.pause.paused:
                            self.show_entities()
                        else:
                            self.hide_entities()

    # Detect collisions between Pac-Man and ghosts.
    # If a ghost is in freight mode, send it back to the ghost house (spawn mode).
    def check_ghost_events(self):
        for ghost in self.ghosts:
            if self.pacman.collide_ghost(ghost):
                if ghost.mode.current is FREIGHT:
                    self.pacman.visible = False
                    ghost.visible = False
                    self.pause.set_pause(pauseTime=1, func=self.show_entities)
                    ghost.start_spawn()
                    self.nodes.allow_home_access(ghost)
                elif ghost.mode.current is not SPAWN:
                    if self.pacman.alive:
                        self.lives -= 1
                        self.pacman.die()
                        self.ghosts.hide()
                        if self.lives <= 0:
                            self.pause.set_pause(pauseTime=3, func=self.restart_game)
                        else:
                            self.pause.set_pause(pauseTime=3, func=self.reset_level)

    # Controls fruit appearance and collision with Pac-Man.
    # Fruit appears after eating 50 or 140 pellets.
    def check_fruit_events(self):
        if self.pellets.numEaten in [50, 140] and self.fruit is None:
            self.fruit = Fruit(self.nodes.get_node_from_tiles(9, 20))
        if self.fruit is not None:
            if self.pacman.collide_check(self.fruit) or self.fruit.destroy:
                self.fruit = None

    # Detects if Pac-Man has eaten a pellet.
    # Removes pellet, increments counter, and triggers ghost freight mode if it's a power pellet.
    def check_pellet_events(self):
        pellet = self.pacman.eat_pellets(self.pellets.pelletList)
        if pellet:
            self.pellets.numEaten += 1

            if self.pellets.numEaten == 30:
                self.ghosts.inky.startNode.allow_access(RIGHT, self.ghosts.inky)
            if self.pellets.numEaten == 70:
                self.ghosts.clyde.startNode.allow_access(LEFT, self.ghosts.clyde)

            self.pellets.pelletList.remove(pellet)

            if pellet.name == POWERPELLET:
                self.ghosts.start_freight()

            if self.pellets.is_empty():
                self.hide_entities()
                self.pause.set_pause(pauseTime=3, func=self.next_level)

    # Makes Pac-Man and ghosts visible (after unpausing or level start).
    def show_entities(self):
        self.pacman.visible = True
        self.ghosts.show()

    # Hides all entities (used during pause or transitions).
    def hide_entities(self):
        self.pacman.visible = False
        self.ghosts.hide()

    # Draws all game elements to the screen each frame:
    # background, maze, pellets, fruit, Pac-Man, and ghosts.
    def render(self):
        self.screen.blit(self.background, (0, 0))
        self.nodes.render(self.screen)
        self.pellets.render(self.screen)

        if self.fruit is not None:
            self.fruit.render(self.screen)

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
