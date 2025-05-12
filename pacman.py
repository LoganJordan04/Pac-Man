import pygame
from pygame.locals import *
from vector import Vector2
from constants import *


# The main player class representing Pac-Man. Handles movement input,
# position updating, and rendering the character on screen.
class Pacman(object):
    def __init__(self, node):
        self.name = PACMAN

        self.directions = {STOP: Vector2(), UP: Vector2(0, -1), DOWN: Vector2(0, 1), LEFT: Vector2(-1, 0),
                           RIGHT: Vector2(1, 0)}
        self.direction = STOP
        self.speed = 100 * TILEWIDTH / 16
        self.radius = 10
        self.color = YELLOW
        self.node = node
        self.set_position()

    def set_position(self):
        self.position = self.node.position.copy()

    def update(self, dt):
        #self.position += self.directions[self.direction]*self.speed*dt
        direction = self.get_valid_key()
        self.direction = direction
        self.node = self.get_new_target(direction)
        self.set_position()

    def valid_direction(self, direction):
        if direction is not STOP:
            if self.node.neighbors[direction] is not None:
                return True
        return False

    def get_new_target(self, direction):
        if self.valid_direction(direction):
            return self.node.neighbors[direction]
        return self.node

    # Checks for user key presses and returns a movement direction.
    def get_valid_key(self):
        key_pressed = pygame.key.get_pressed()

        # Up arrow or W
        if key_pressed[K_UP] or key_pressed[K_w]:
            return UP
        # Down arrow or S
        if key_pressed[K_DOWN] or key_pressed[K_s]:
            return DOWN
        # Left arrow or A
        if key_pressed[K_LEFT] or key_pressed[K_a]:
            return LEFT
        # Right arrow or D
        if key_pressed[K_RIGHT] or key_pressed[K_d]:
            return RIGHT

        return STOP

    # Draw Pac-Man on the game screen.
    def render(self, screen):
        # Convert float position to integer pixel coordinates
        p = self.position.as_int()

        # Draw Pac-Man as a yellow circle
        pygame.draw.circle(screen, self.color, p, self.radius)
