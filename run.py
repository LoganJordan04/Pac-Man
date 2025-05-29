import pygame
from pygame.locals import *
from constants import *
from pacman import Pacman
from nodes import NodeGroup
from pellets import PelletGroup
from ghosts import GhostGroup
from fruit import Fruit
from pauser import Pause
from text import TextGroup
from sprites import LifeSprites
from sprites import MazeSprites


# Main game controller class: handles setup, updates, input, collisions, and rendering
class GameController(object):
    def __init__(self):
        pygame.init()

        # Create the main display surface using screen size defined in constants.py
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)

        # Sets the default maze background
        self.background = None
        self.background_norm = None
        self.background_flash = None

        # Clock to manage time between frames and limit frame rate
        self.clock = pygame.time.Clock()

        # Bonus fruit object (appears temporarily)
        self.fruit = None
        self.fruitCaptured = []

        # Pause manager for delays and manual pauses
        self.pause = Pause(True)

        # Current level and remaining lives
        self.level = 0
        self.lives = 5
        self.lifesprites = LifeSprites(self.lives)

        self.score = 0
        self.textgroup = TextGroup()

        # Maze flash (when completing a level) and the active timer
        self.flashBG = False
        self.flashTime = 0.2
        self.flashTimer = 0


    # Restarts the game from level 0 with full lives after game over.
    def restart_game(self):
        self.lives = 5
        self.level = 0
        self.pause.paused = True
        self.fruit = None
        self.fruitCaptured = []
        self.start_game()
        self.score = 0
        self.textgroup.update_score(self.score)
        self.textgroup.update_level(self.level)
        self.textgroup.show_text(READYTXT)
        self.lifesprites.reset_lives(self.lives)

    # Resets the current level after a player death (if lives remain).
    def reset_level(self):
        self.pause.paused = True
        self.pacman.reset()
        self.ghosts.reset()
        self.fruit = None
        self.textgroup.show_text(READYTXT)

    # Called when all pellets are eaten.
    # Advances to the next level and resets game entities.
    def next_level(self):
        self.show_entities()
        self.level += 1
        self.pause.paused = True
        self.start_game()
        self.textgroup.update_level(self.level)

    # Builds the background surface for the maze.
    # Loads the maze layout and rotation files, constructs the tilemap.
    def set_background(self):
        self.background_norm = pygame.surface.Surface(SCREENSIZE).convert()
        self.background_norm.fill(BLACK)

        self.background_flash = pygame.surface.Surface(SCREENSIZE).convert()
        self.background_flash.fill(BLACK)

        self.background_norm = self.mazesprites.construct_background(self.background_norm, self.level % 5)
        self.background_flash = self.mazesprites.construct_background(self.background_flash, 5)

        self.flashBG = False
        self.background = self.background_norm

    # Called once at game start. Initializes maze, Pac-Man, ghosts, and pellets.
    # Loads the maze from file, places all entities, and sets up portals and ghost house.
    def start_game(self):
        self.mazesprites = MazeSprites("maze1.txt", "maze1_rotation.txt")
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

        self.textgroup.update(dt)

        # Animate flashing pellets (power pellets)
        self.pellets.update(dt)

        if not self.pause.paused:
            # Update entity movement and animation
            self.ghosts.update(dt)
            if self.fruit is not None:
                self.fruit.update(dt)

            # Handle pellet consumption and score tracking
            self.check_pellet_events()

            # Handle ghost collisions and mode logic
            self.check_ghost_events()

            # Handle fruit consumption and spawning
            self.check_fruit_events()

        if self.pacman.alive:
            if not self.pause.paused:
                self.pacman.update(dt)
        else:
            self.pacman.update(dt)

        # Handle level flashing when all pellets are eaten
        if self.flashBG:
            self.flashTimer += dt
            if self.flashTimer >= self.flashTime:
                self.flashTimer = 0
                if self.background == self.background_norm:
                    self.background = self.background_flash
                else:
                    self.background = self.background_norm

        afterPauseMethod = self.pause.update(dt)
        if afterPauseMethod is not None:
            afterPauseMethod()

        # Handle user inputs or system quit events
        self.check_events()

        # Draw updated frame to screen
        self.render()

    def update_score(self, points):
        self.score += points
        self.textgroup.update_score(self.score)

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
                            self.textgroup.hide_text()
                            self.show_entities()
                        else:
                            self.textgroup.show_text(PAUSETXT)
                            self.hide_entities()

    # Detect collisions between Pac-Man and ghosts.
    # If a ghost is in freight mode, send it back to the ghost house (spawn mode).
    def check_ghost_events(self):
        for ghost in self.ghosts:
            if self.pacman.collide_ghost(ghost):
                if ghost.mode.current is FREIGHT:
                    self.pacman.visible = False
                    ghost.visible = False
                    self.update_score(ghost.points)
                    self.textgroup.add_text(str(ghost.points), WHITE, ghost.position.x, ghost.position.y, 8, time=1)
                    self.ghosts.update_points()
                    self.pause.set_pause(pauseTime=1, func=self.show_entities)
                    ghost.start_spawn()
                    self.nodes.allow_home_access(ghost)
                elif ghost.mode.current is not SPAWN:
                    if self.pacman.alive:
                        self.lives -= 1
                        self.lifesprites.remove_image()
                        self.pacman.die()
                        self.ghosts.hide()
                        if self.lives <= 0:
                            self.textgroup.show_text(GAMEOVERTXT)
                            self.pause.set_pause(pauseTime=3, func=self.restart_game)
                        else:
                            self.pause.set_pause(pauseTime=3, func=self.reset_level)

    # Controls fruit appearance and collision with Pac-Man.
    # Fruit appears after eating 50 or 140 pellets.
    def check_fruit_events(self):
        if self.pellets.numEaten == 50 or self.pellets.numEaten == 140:
            if self.fruit is None:
                self.fruit = Fruit(self.nodes.get_node_from_tiles(9, 20))
                print(self.fruit)
        if self.fruit is not None:
            if self.pacman.collide_check(self.fruit):
                self.update_score(self.fruit.points)
                self.textgroup.add_text(str(self.fruit.points), WHITE, self.fruit.position.x, self.fruit.position.y, 8, time=1)

                # Capturing the fruit
                fruitCaptured = False
                for fruit in self.fruitCaptured:
                    if fruit.get_offset() == self.fruit.image.get_offset():
                        fruitCaptured = True
                        break
                if not fruitCaptured:
                    self.fruitCaptured.append(self.fruit.image)

                self.fruit = None
            elif self.fruit.destroy:
                self.fruit = None

    # Detects if Pac-Man has eaten a pellet.
    # Removes pellet, increments counter, triggers ghost freight mode if it's a power pellet,
    # and checks if all pellets are eaten.
    def check_pellet_events(self):
        pellet = self.pacman.eat_pellets(self.pellets.pelletList)
        if pellet:
            self.pellets.numEaten += 1
            self.update_score(pellet.points)

            if self.pellets.numEaten == 30:
                self.ghosts.inky.startNode.allow_access(RIGHT, self.ghosts.inky)
            if self.pellets.numEaten == 70:
                self.ghosts.clyde.startNode.allow_access(LEFT, self.ghosts.clyde)

            self.pellets.pelletList.remove(pellet)

            if pellet.name == POWERPELLET:
                self.ghosts.start_freight()

            if self.pellets.is_empty():
                self.flashBG = True
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
    # background, maze, pellets, fruit, Pac-Man, ghosts, and lives.
    def render(self):
        self.screen.blit(self.background, (0, 0))
        self.pellets.render(self.screen)

        if self.fruit is not None:
            self.fruit.render(self.screen)

        self.pacman.render(self.screen)
        self.ghosts.render(self.screen)

        self.textgroup.render(self.screen)

        for i in range(len(self.lifesprites.images)):
            x = self.lifesprites.images[i].get_width() * i
            y = SCREENHEIGHT - self.lifesprites.images[i].get_height()
            self.screen.blit(self.lifesprites.images[i], (x, y))

        for i in range(len(self.fruitCaptured)):
            x = SCREENWIDTH - self.fruitCaptured[i].get_width() * (i + 1)
            y = SCREENHEIGHT - self.fruitCaptured[i].get_height()
            self.screen.blit(self.fruitCaptured[i], (x, y))

        # Refresh the screen with the new frame
        pygame.display.update()


# Entry point for the game: creates and starts the main loop
if __name__ == "__main__":
    game = GameController()
    game.start_game()

    # Main loop runs until manually exited
    while True:
        game.update()
