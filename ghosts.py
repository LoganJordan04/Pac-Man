import pygame
from pygame.locals import *
from vector import Vector2
from constants import *
from entity import Entity
from modes import ModeController


# Represents a ghost entity in the game.
# Inherits basic movement behavior from Entity and adds AI decision-making
# through modes based on the ModeController.
class Ghost(Entity):
    def __init__(self, node, pacman=None, blinky=None):
        super().__init__(node)
        self.name = GHOST

        # Score value when eaten
        self.points = 200

        # Target position for AI pathfinding
        self.goal = Vector2()

        # Ghosts use goal-based AI instead of random movement
        self.directionMethod = self.goal_direction

        # Reference to Pac-Man for chase mode
        self.pacman = pacman

        # Controls modes
        self.mode = ModeController(self)

        # Starting position of the ghost
        self.homeNode = node

        # Optional reference to Blinky (used by Inky)
        self.blinky = blinky

    # Resets the ghost to its default behavior and appearance after level restart.
    def reset(self):
        Entity.reset(self)
        self.points = 200
        self.directionMethod = self.goal_direction

    # Chooses the direction that brings the ghost closest to its current goal.
    # Compares squared distances to avoid expensive square roots.
    def goal_direction(self, directions):
        distances = []
        for direction in directions:
            vec = self.node.position + self.directions[direction] * TILEWIDTH - self.goal
            distances.append(vec.magnitude_squared())

        # Choose the direction that minimizes distance to the goal
        index = distances.index(min(distances))
        return directions[index]

    # Called every frame to update ghost logic and movement.
    # Applies AI mode logic before standard position update.
    def update(self, dt):
        # Handle timing and transitions between modes
        self.mode.update(dt)

        if self.mode.current is SCATTER:
            self.scatter()
        elif self.mode.current is CHASE:
            self.chase()

        # Apply standard movement logic from Entity
        super().update(dt)

    # Scatter mode: ghost retreats to its corner or default location.
    def scatter(self):
        self.goal = Vector2()

    # Chase mode: ghost actively pursues Pac-Man's current position.
    def chase(self):
        self.goal = self.pacman.position

    # Enter freight mode where ghost runs away and becomes vulnerable
    def start_freight(self):
        self.mode.set_freight_mode()
        if self.mode.current == FREIGHT:
            self.set_speed(50)
            self.directionMethod = self.random_direction

    # Return to normal speed and chasing logic after freight ends
    def normal_mode(self):
        self.set_speed(100)
        self.directionMethod = self.goal_direction

    # Target the spawn location (used after being eaten)
    def spawn(self):
        self.goal = self.spawnNode.position

    # Assign a spawn location node
    def set_spawn_node(self, node):
        self.spawnNode = node

    # Begin spawn mode (returning to base after being eaten)
    def start_spawn(self):
        self.mode.set_spawn_mode()
        if self.mode.current == SPAWN:
            self.set_speed(150)
            self.directionMethod = self.goal_direction
            self.spawn()


# Blinky always targets Pac-Man directly during chase
class Blinky(Ghost):
    def __init__(self, node, pacman=None, blinky=None):
        Ghost.__init__(self, node, pacman, blinky)
        self.name = BLINKY
        self.color = RED


# Pinky targets 4 tiles ahead of Pac-Man
class Pinky(Ghost):
    def __init__(self, node, pacman=None, blinky=None):
        Ghost.__init__(self, node, pacman, blinky)
        self.name = PINKY
        self.color = PINK

    def scatter(self):
        self.goal = Vector2(TILEWIDTH*NCOLS, 0)

    def chase(self):
        self.goal = self.pacman.position + self.pacman.directions[self.pacman.direction] * TILEWIDTH * 4


# Inky uses a vector from Blinky to a point 2 tiles ahead of Pac-Man, then doubles it
class Inky(Ghost):
    def __init__(self, node, pacman=None, blinky=None):
        Ghost.__init__(self, node, pacman, blinky)
        self.name = INKY
        self.color = TEAL

    def scatter(self):
        self.goal = Vector2(TILEWIDTH*NCOLS, TILEHEIGHT*NROWS)

    def chase(self):
        vec1 = self.pacman.position + self.pacman.directions[self.pacman.direction] * TILEWIDTH * 2
        vec2 = (vec1 - self.blinky.position) * 2
        self.goal = self.blinky.position + vec2


# Clyde chases Pac-Man unless he’s close, then runs to the corner
class Clyde(Ghost):
    def __init__(self, node, pacman=None, blinky=None):
        Ghost.__init__(self, node, pacman, blinky)
        self.name = CLYDE
        self.color = ORANGE

    def scatter(self):
        self.goal = Vector2(0, TILEHEIGHT*NROWS)

    def chase(self):
        d = self.pacman.position - self.position
        ds = d.magnitude_squared()
        if ds <= (TILEWIDTH * 8)**2:
            self.scatter()
        else:
            self.goal = self.pacman.position + self.pacman.directions[self.pacman.direction] * TILEWIDTH * 4


# Manages all four ghosts and their collective behavior
class GhostGroup(object):
    def __init__(self, node, pacman):
        self.blinky = Blinky(node, pacman)
        self.pinky = Pinky(node, pacman)
        self.inky = Inky(node, pacman, self.blinky)
        self.clyde = Clyde(node, pacman)
        self.ghosts = [self.blinky, self.pinky, self.inky, self.clyde]

    def __iter__(self):
        return iter(self.ghosts)

    def update(self, dt):
        for ghost in self:
            ghost.update(dt)

    def start_freight(self):
        for ghost in self:
            ghost.start_freight()
        self.reset_points()

    def set_spawn_node(self, node):
        for ghost in self:
            ghost.set_spawn_node(node)

    def update_points(self):
        for ghost in self:
            # Each successive ghost is worth double
            ghost.points *= 2

    def reset_points(self):
        for ghost in self:
            ghost.points = 200

    def reset(self):
        for ghost in self:
            ghost.reset()

    def hide(self):
        for ghost in self:
            ghost.visible = False

    def show(self):
        for ghost in self:
            ghost.visible = True

    def render(self, screen):
        for ghost in self:
            ghost.render(screen)
