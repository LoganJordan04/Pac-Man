import pygame
from pygame.locals import *
from vector import Vector2
from constants import *


# The main player class representing Pac-Man.
# Handles movement between nodes, user input, and rendering.
class Pacman(object):
    def __init__(self, node):
        self.name = PACMAN

        # Direction vectors mapped to constants
        self.directions = {
            STOP: Vector2(),
            UP: Vector2(0, -1),
            DOWN: Vector2(0, 1),
            LEFT: Vector2(-1, 0),
            RIGHT: Vector2(1, 0)
        }

        # Initial movement direction
        self.direction = STOP

        # Movement speed scaled to tile size
        self.speed = 100 * TILEWIDTH / 16

        # Drawing Pac-Man
        # WILL BE REPLACED LATER
        self.radius = 10
        self.color = YELLOW

        # Initialize position of Pac-Man
        # Sets the current node and the target node Pac-Man is moving toward
        self.node = node
        self.set_position()
        self.target = node

    # Sets Pac-Man's pixel position to match the current node position.
    def set_position(self):
        self.position = self.node.position.copy()

    # Called every frame to update Pac-Man's position and handle direction input.
    # Uses delta time (dt) for frame-rate-independent movement.
    def update(self, dt):
        self.position += self.directions[self.direction] * self.speed * dt

        # Get current input direction
        direction = self.get_valid_key()

        # Check if Pac-Man has passed the target node
        if self.overshoot_target():
            # Snap to target node
            self.node = self.target

            # Try new input direction
            self.target = self.get_new_target(direction)

            # If new input is valid, use it; otherwise keep going in current direction
            if self.target is not self.node:
                self.direction = direction
            else:
                self.target = self.get_new_target(self.direction)

            # Stop if no valid target in current direction
            if self.target is self.node:
                self.direction = STOP

            # Align Pac-Man to node
            self.set_position()

        else:
            # Allow immediate reversal of direction if opposite is pressed
            if self.opposite_direction(direction):
                self.reverse_direction()

    # Returns True if the given direction leads to a connected neighbor node.
    def valid_direction(self, direction):
        if direction is not STOP:
            if self.node.neighbors[direction] is not None:
                return True
        return False

    # Returns the neighbor node in the given direction if it's valid.
    # If not valid, returns current node (i.e., no movement).
    def get_new_target(self, direction):
        if self.valid_direction(direction):
            return self.node.neighbors[direction]
        return self.node

    # Returns a movement direction constant based on user key presses.
    # Supports both arrow keys and WASD.
    def get_valid_key(self):
        key_pressed = pygame.key.get_pressed()

        if key_pressed[K_UP] or key_pressed[K_w]:
            return UP
        if key_pressed[K_DOWN] or key_pressed[K_s]:
            return DOWN
        if key_pressed[K_LEFT] or key_pressed[K_a]:
            return LEFT
        if key_pressed[K_RIGHT] or key_pressed[K_d]:
            return RIGHT

        return STOP

    # Draws Pac-Man on the screen as a yellow circle at his current position.
    # WILL BE REPLACED LATER
    def render(self, screen):
        p = self.position.as_int()
        pygame.draw.circle(screen, self.color, p, self.radius)

    # Returns True if Pac-Man has moved past his target node.
    # Helps snap him to the node and evaluate next movement choice.
    def overshoot_target(self):
        if self.target is not None:
            vec1 = self.target.position - self.node.position
            vec2 = self.position - self.node.position
            node2Target = vec1.magnitude_squared()
            node2Self = vec2.magnitude_squared()
            return node2Self >= node2Target
        return False

    # Reverses Pac-Man’s movement by swapping current and target nodes and flipping the direction vector.
    def reverse_direction(self):
        self.direction *= -1
        temp = self.node
        self.node = self.target
        self.target = temp

    # Returns True if the given direction is exactly opposite the current direction.
    # Used to allow quick reversals.
    def opposite_direction(self, direction):
        if direction is not STOP:
            if direction == self.direction * -1:
                return True
        return False

    def render(self, screen):
        p = self.position.as_int()
        pygame.draw.circle(screen, self.color, p, self.radius)