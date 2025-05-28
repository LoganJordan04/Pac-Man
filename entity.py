import pygame
from pygame.locals import *
from vector import Vector2
from constants import *
from random import randint


# Base class for all movable characters in the game (e.g., Pac-Man, ghosts).
# Manages movement across the maze, rendering, and basic AI direction logic.
class Entity(object):
    def __init__(self, node):
        self.name = None
        self.image = None

        # Define movement vectors for each direction
        self.directions = {
            UP: Vector2(0, -1),
            DOWN: Vector2(0, 1),
            LEFT: Vector2(-1, 0),
            RIGHT: Vector2(1, 0),
            STOP: Vector2()}

        # Initial movement direction and speed
        self.direction = STOP
        self.set_speed(100)

        # Drawing the entities
        # WILL BE REPLACED LATER
        self.radius = 10
        self.color = WHITE

        # Collision radius for detecting collisions
        self.collideRadius = 5

        # Whether to draw this entity or enable portal teleportation
        self.visible = True
        self.disablePortal = False

        # Optional goal node (e.g. ghost AI)
        self.goal = None

        # Direction decision logic (default is random)
        self.direction_method = self.goal_direction

        # Initialize position and node tracking
        self.set_start_node(node)

    # Sets the starting node and resets position and movement tracking.
    def set_start_node(self, node):
        self.node = node
        self.startNode = node
        self.target = node
        self.set_position()

    # Fully resets the entity to its original state.
    def reset(self):
        self.set_start_node(self.startNode)
        self.direction = STOP
        self.speed = 100
        self.visible = True

    # Places the entity halfway between its current node and the neighbor in the specified direction.
    # Used for initializing start positions.
    def set_between_nodes(self, direction):
        if self.node.neighbors[direction] is not None:
            self.target = self.node.neighbors[direction]
            self.position = (self.node.position + self.target.position) / 2.0

    # Align entity's pixel position to its current node position.
    def set_position(self):
        self.position = self.node.position.copy()

    # Update entity position and handle target transitions each frame.
    def update(self, dt):
        self.position += self.directions[self.direction] * self.speed * dt

        if self.overshot_target():
            self.node = self.target

            # Get all possible directions (excluding reverse)
            directions = self.valid_directions()

            # Choose next direction based on AI or randomness
            direction = self.direction_method(directions)

            # Handle teleportation through portal nodes
            if not self.disablePortal and self.node.neighbors[PORTAL] is not None:
                self.node = self.node.neighbors[PORTAL]

            # Set next target node and direction
            self.target = self.get_new_target(direction)
            if self.target is not self.node:
                self.direction = direction
            else:
                # If stuck, keep trying the same direction
                self.target = self.get_new_target(self.direction)

            # Snap to node to avoid floating point drift
            self.set_position()

    # Check if the given direction leads to a valid neighboring node.
    def valid_direction(self, direction):
        if direction is not STOP:
            if self.name in self.node.access[direction]:
                if self.node.neighbors[direction] is not None:
                    return True
        return False

    # Returns a list of all valid directions (excluding reverse).
    def valid_directions(self):
        directions = []
        for key in [UP, DOWN, LEFT, RIGHT]:
            if self.valid_direction(key):
                if key != self.direction * -1:
                    directions.append(key)

        # If no direction available, reverse
        if len(directions) == 0:
            directions.append(self.direction * -1)

        return directions

    # Default direction strategy: randomly choose one from the available directions.
    def random_direction(self, directions):
        return directions[randint(0, len(directions) - 1)]

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
            node2Target = vec1.magnitude_squared()
            node2Self = vec2.magnitude_squared()
            return node2Self >= node2Target
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

    # Chooses the direction that brings the entity closest to its goal.
    # Used by ghosts in CHASE or SCATTER modes.
    def goal_direction(self, directions):
        distances = []
        for direction in directions:
            vec = self.node.position + self.directions[direction] * TILEWIDTH - self.goal
            distances.append(vec.magnitude_squared())

        index = distances.index(min(distances))
        return directions[index]

    # Render the entity as a colored circle
    # WILL BE UPDATED LATER
    def render(self, screen):
        if self.visible:
            if self.image is not None:
                screen.blit(self.image, self.position.as_tuple())
            else:
                p = self.position.as_int()
                pygame.draw.circle(screen, self.color, p, self.radius)
