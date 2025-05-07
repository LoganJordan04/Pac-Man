import pygame
from pygame.locals import *
from vector import Vector2
from constants import *


# The main player class representing Pac-Man. Handles movement input,
# position updating, and rendering the character on screen.
class Pacman(object):
    # Set character identity (useful for debugging or logic checks)
    def __init__(self):
        self.name = PACMAN

        # Initial position of Pac-Man (manually placed for starting point)
        self.position = Vector2(200, 400)

        # Dictionary mapping directions to vector representations
        self.directions = {
            # No movement
            STOP: Vector2(),
            # Move up
            UP: Vector2(0, -1),
            # Move down
            DOWN: Vector2(0, 1),
            # Move left
            LEFT: Vector2(-1, 0),
            # Move right
            RIGHT: Vector2(1, 0)
        }

        # Start with no movement
        self.direction = STOP

        # Speed of Pac-Man, scaled to tile width (default speed tuning)
        self.speed = 100 * TILEWIDTH / 16

        # Radius of Pac-Man's drawn circle and color
        self.radius = 10
        self.color = YELLOW

    # Update Pac-Man's position and handle directional input.
    def update(self, dt):
        # Move Pac-Man in the current direction by speed * delta_time
        self.position += self.directions[self.direction] * self.speed * dt

        # Get the latest valid key press and update movement direction
        direction = self.get_valid_key()
        self.direction = direction

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
