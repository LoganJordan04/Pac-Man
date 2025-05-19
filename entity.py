import pygame
from pygame.locals import *
from vector import Vector2
from constants import *
from random import randint


# Base class for all moving characters (Pac-Man, ghosts).
# Manages direction-based movement across the node graph, target tracking, and rendering.
class Entity(object):
    def __init__(self, node):
        self.name = None

        # Define movement vectors for each direction
        self.directions = {
            UP: Vector2(0, -1),
            DOWN: Vector2(0, 1),
            LEFT: Vector2(-1, 0),
            RIGHT: Vector2(1, 0),
            STOP: Vector2()}

        # Initial movement direction
        self.direction = STOP

        # Default movement speed
        self.set_speed(100)

        # Drawing the entities
        # WILL BE REPLACED LATER
        self.radius = 10
        self.color = RED

        # Initialize position of entity
        # Sets the current node and the target node entity is moving toward
        self.node = node
        self.set_position()
        self.target = node

        # Collision radius for detecting collisions
        self.collideRadius = 5

        # Whether to draw this entity or enable portal teleportation
        self.visible = True
        self.disablePortal = False

        # Optional goal node (e.g. ghost AI)
        self.goal = None

        # Direction decision logic (default is random)
        self.directionMethod = self.random_direction

    # Align entity's pixel position to its current node position.
    def set_position(self):
        self.position = self.node.position.copy()

    # Check if the given direction leads to a valid neighboring node.
    def valid_direction(self, direction):
        return direction is not STOP and self.node.neighbors[direction] is not None

    # Return the neighboring node in the given direction, or the current node if invalid.
    def get_new_target(self, direction):
        if self.valid_direction(direction):
            return self.node.neighbors[direction]
        return self.node

    # Determine if the entity has passed its target node.
    # Used to trigger snapping and next movement decision.
    def overshot_target(self):
        if self.target is not None:
            vec1 = self.target.position - self.node.position
            vec2 = self.position - self.node.position
            return vec2.magnitude_squared() >= vec1.magnitude_squared()
        return False

    # Reverses movement by swapping current and target nodes and flipping the direction vector.
    def reverse_direction(self):
        self.direction *= -1
        temp = self.node
        self.node = self.target
        self.target = temp

    # Returns True if given direction is directly opposite the current direction.
    def opposite_direction(self, direction):
        if direction is not STOP:
            if direction == self.direction * -1:
                return True
        return False

    # Set entity movement speed (scaled to tile width).
    def set_speed(self, speed):
        self.speed = speed * TILEWIDTH / 16

    # Render the entity as a colored circle/
    # WILL BE UPDATED LATER
    def render(self, screen):
        if self.visible:
            p = self.position.as_int()
            pygame.draw.circle(screen, self.color, p, self.radius)

    # Update entity position and handle target transitions each frame.
    def update(self, dt):
        self.position += self.directions[self.direction] * self.speed * dt

        if self.overshot_target():
            self.node = self.target

            # Get all possible directions (excluding reverse)
            directions = self.valid_directions()

            # Choose next direction based on AI or randomness
            direction = self.directionMethod(directions)

            # Handle teleportation through portal nodes
            if not self.disablePortal and self.node.neighbors[PORTAL] is not None:
                self.node = self.node.neighbors[PORTAL]

            # Set next target node and direction
            self.target = self.get_new_target(direction)
            if self.target is not self.node:
                self.direction = direction
            else:
                self.target = self.get_new_target(self.direction)

            # Snap to node to avoid floating point drift
            self.set_position()

    # Returns a list of all valid directions (excluding reverse).
    def valid_directions(self):
        directions = []
        for direction in [UP, DOWN, LEFT, RIGHT]:
            if self.valid_direction(direction) and direction != self.direction * -1:
                directions.append(direction)

        # If no direction available, reverse
        if not directions:
            directions.append(self.direction * -1)

        return directions

    # Default direction strategy: randomly choose one from the available directions.
    def random_direction(self, directions):
        return directions[randint(0, len(directions) - 1)]
