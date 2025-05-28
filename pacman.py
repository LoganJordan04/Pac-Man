import pygame
from pygame.locals import *
from vector import Vector2
from constants import *
from entity import Entity
from sprites import PacmanSprites


# The main player class representing Pac-Man.
# Handles movement between nodes, user input, and rendering.
class Pacman(Entity):
    def __init__(self, node):
        super().__init__(node)
        self.name = PACMAN

        # Direction vectors mapped to constants
        self.directions = {
            STOP: Vector2(),
            UP: Vector2(0, -1),
            DOWN: Vector2(0, 1),
            LEFT: Vector2(-1, 0),
            RIGHT: Vector2(1, 0)
        }

        # Default movement direction and speed
        self.direction = LEFT
        self.speed = 100 * TILEWIDTH / 16

        # Start Pac-Man between current node and neighbor in the given direction
        self.set_between_nodes(LEFT)

        # Drawing Pac-Man
        # WILL BE REPLACED LATER
        self.radius = 10
        self.color = YELLOW

        self.sprites = PacmanSprites(self)

        # Initialize position of Pac-Man
        # Sets the current node and the target node Pac-Man is moving toward
        self.node = node
        self.set_position()
        self.target = node

        # Collision radius used for interacting with pellets and ghosts
        self.collideRadius = 5

        # Flag indicating if Pac-Man is alive
        self.alive = True

    # Resets Pac-Man to the starting state (after death or level reset).
    def reset(self):
        Entity.reset(self)
        self.direction = LEFT
        self.set_between_nodes(LEFT)
        self.alive = True

    # Handles Pac-Man's death by stopping movement and marking him as not alive.
    def die(self):
        self.alive = False
        self.direction = STOP

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

            # If entering a portal, jump to the next node
            if self.node.neighbors[PORTAL] is not None:
                self.node = self.node.neighbors[PORTAL]

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
        return direction is not STOP and self.node.neighbors[direction] is not None

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
    # WILL BE UPDATED LATER
    def render(self, screen):
        p = self.position.as_int()
        pygame.draw.circle(screen, self.color, p, self.radius)

    # Returns True if Pac-Man has moved past his target node.
    # Prevents floating-point imprecision and ensures snapping to nodes.
    def overshoot_target(self):
        if self.target is not None:
            vec1 = self.target.position - self.node.position
            vec2 = self.position - self.node.position
            return vec2.magnitude_squared() >= vec1.magnitude_squared()
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
        return direction is not STOP and direction == self.direction * -1

    # Checks if Pac-Man is colliding with any pellet in the given list.
    # Returns the first pellet eaten (for removal and scoring).
    def eat_pellets(self, pelletList):
        for pellet in pelletList:
            if self.collide_check(pellet):
                return pellet
        return None

    # Check for a collision between Pac-Man and a ghost.
    def collide_ghost(self, ghost):
        return self.collide_check(ghost)

    # Performs a circular collision check between Pac-Man and another entity (pellet or ghost).
    def collide_check(self, other):
        d = self.position - other.position
        dSquared = d.magnitude_squared()
        rSquared = (self.collideRadius + other.collideRadius) ** 2
        if dSquared <= rSquared:
            return True
        return False
