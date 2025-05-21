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
    def __init__(self, node, pacman=None):
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

    def start_freight(self):
        self.mode.set_freight_mode()
        if self.mode.current == FREIGHT:
            self.set_speed(50)
            self.directionMethod = self.random_direction

    def normal_mode(self):
        self.set_speed(100)
        self.directionMethod = self.goal_direction
