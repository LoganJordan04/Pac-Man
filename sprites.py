import pygame
from constants import *
import numpy as np
from animation import Animator

# Base dimensions of a tile in the spritesheet (used for scaling to screen resolution)
BASETILEWIDTH = 16
BASETILEHEIGHT = 16

# Constant for death animation key
DEATH = 5


# Spritesheet class handles loading and extracting individual sprite images from the full spritesheet.
class Spritesheet(object):
    def __init__(self):
        # Load the spritesheet image file
        self.sheet = pygame.image.load("spritesheet.png").convert()

        # Set transparency color to top-left pixel
        transcolor = self.sheet.get_at((0, 0))
        self.sheet.set_colorkey(transcolor)

        # Scale spritesheet to match current TILEWIDTH and TILEHEIGHT settings
        width = int(self.sheet.get_width() / BASETILEWIDTH * TILEWIDTH)
        height = int(self.sheet.get_height() / BASETILEHEIGHT * TILEHEIGHT)
        self.sheet = pygame.transform.scale(self.sheet, (width, height))

    # Extracts a rectangular section from the spritesheet at tile-based coordinates (x, y) and returns it as a surface.
    def get_image(self, x, y, width, height):
        x *= TILEWIDTH
        y *= TILEHEIGHT
        self.sheet.set_clip(pygame.Rect(x, y, width, height))
        return self.sheet.subsurface(self.sheet.get_clip())


# Handles loading and assigning sprites for Pac-Man.
class PacmanSprites(Spritesheet):
    def __init__(self, entity):
        super().__init__()
        self.entity = entity
        self.entity.image = self.get_start_image()

        self.animations = {}
        self.define_animations()

        # Default "mouth closed" sprite
        self.stopimage = (8, 0)

    # Loads Pac-Man's default sprite (e.g., mouth closed at starting position).
    def get_start_image(self):
        return self.get_image(8, 0)

    # Returns a specific Pac-Man sprite at grid (x, y) on the sheet.
    def get_image(self, x, y):
        return super().get_image(x, y, 2 * TILEWIDTH, 2 * TILEHEIGHT)

    # Define animation sequences for Pac-Man's directional movement and death
    def define_animations(self):
        self.animations[LEFT] = Animator(((8, 0), (0, 0), (0, 2), (0, 0)))
        self.animations[RIGHT] = Animator(((10, 0), (2, 0), (2, 2), (2, 0)))
        self.animations[UP] = Animator(((10, 2), (6, 0), (6, 2), (6, 0)))
        self.animations[DOWN] = Animator(((8, 2), (4, 0), (4, 2), (4, 0)))

        self.animations[DEATH] = Animator(
            ((0, 12), (2, 12), (4, 12), (6, 12), (8, 12), (10, 12),
             (12, 12), (14, 12), (16, 12), (18, 12), (20, 12)),
            speed=6, loop=False
        )

    # Updates the current animation frame based on movement direction or death
    def update(self, dt):
        if self.entity.alive:
            if self.entity.direction in self.animations:
                self.entity.image = self.get_image(*self.animations[self.entity.direction].update(dt))
                self.stopimage = self.animations[self.entity.direction].frames[0]
            elif self.entity.direction == STOP:
                self.entity.image = self.get_image(*self.stopimage)
        else:
            self.entity.image = self.get_image(*self.animations[DEATH].update(dt))

    # Reset all animations to initial state
    def reset(self):
        for anim in self.animations.values():
            anim.reset()


# Handles sprite logic for the four ghost characters.
class GhostSprites(Spritesheet):
    def __init__(self, entity):
        super().__init__()

        # X tile index per ghost name
        self.x = {
            BLINKY: 0,
            PINKY: 2,
            INKY: 4,
            CLYDE: 6
        }
        self.entity = entity
        self.entity.image = self.get_start_image()

    # Loads the initial sprite for the ghost based on its type (BLINKY, PINKY, etc.).
    # All start on row 4 of the sheet.
    def get_start_image(self):
        return self.get_image(self.x[self.entity.name], 4)

    # Returns a specific ghost sprite at tile (x, y).
    def get_image(self, x, y):
        return super().get_image(x, y, 2 * TILEWIDTH, 2 * TILEHEIGHT)

    # Update the ghost's animation frame based on direction and mode
    def update(self, dt):
        x = self.x[self.entity.name]

        if self.entity.mode.current in [SCATTER, CHASE]:
            if self.entity.direction == LEFT:
                self.entity.image = self.get_image(x, 8)
            elif self.entity.direction == RIGHT:
                self.entity.image = self.get_image(x, 10)
            elif self.entity.direction == DOWN:
                self.entity.image = self.get_image(x, 6)
            elif self.entity.direction == UP:
                self.entity.image = self.get_image(x, 4)

        elif self.entity.mode.current == FREIGHT:
            self.entity.image = self.get_image(10, 4)

        elif self.entity.mode.current == SPAWN:
            if self.entity.direction == LEFT:
                self.entity.image = self.get_image(8, 8)
            elif self.entity.direction == RIGHT:
                self.entity.image = self.get_image(8, 10)
            elif self.entity.direction == DOWN:
                self.entity.image = self.get_image(8, 6)
            elif self.entity.direction == UP:
                self.entity.image = self.get_image(8, 4)


# Loads the correct fruit sprite based on current level (looped).
class FruitSprites(Spritesheet):
    def __init__(self, entity, level):
        super().__init__()
        self.entity = entity

        # Sprites vary (cherry, strawberry, etc.) based on modulo of level index.
        self.fruits = {0: (16, 8), 1: (18, 8), 2: (20, 8), 3: (16, 10), 4: (18, 10), 5: (20, 10)}
        self.entity.image = self.get_start_image(level % len(self.fruits))

    # Loads the default fruit sprite from the sheet.
    def get_start_image(self, key):
        return self.get_image(*self.fruits[key])

    # Returns a specific fruit sprite from tile (x, y).
    def get_image(self, x, y):
        return super().get_image(x, y, 2 * TILEWIDTH, 2 * TILEHEIGHT)


# Displays Pac-Man lives as icons on screen.
class LifeSprites(Spritesheet):
    def __init__(self, numlives):
        super().__init__()
        self.reset_lives(numlives)

    # Removes one life icon (e.g., after player dies).
    def remove_image(self):
        if self.images:
            self.images.pop(0)

    # Resets the life icons to the specified number.
    def reset_lives(self, numlives):
        self.images = [self.get_image(0, 0) for _ in range(numlives)]

    # Loads a 2x2 tile sprite for Pac-Man's life icon.
    def get_image(self, x, y):
        return super().get_image(x, y, 2 * TILEWIDTH, 2 * TILEHEIGHT)


# Builds and renders the maze tileset from level layout files
class MazeSprites(Spritesheet):
    def __init__(self, mazefile, rotfile):
        super().__init__()
        self.data = self.read_maze_file(mazefile)
        self.rotdata = self.read_maze_file(rotfile)

    def get_image(self, x, y):
        return super().get_image(x, y, TILEWIDTH, TILEHEIGHT)

    # Reads maze layout or rotation info from file
    def read_maze_file(self, mazefile):
        return np.loadtxt(mazefile, dtype='<U1')

    # Assembles the background tile image from layout and rotation maps
    def construct_background(self, background, y):
        for row in range(self.data.shape[0]):
            for col in range(self.data.shape[1]):
                if self.data[row][col].isdigit():
                    x = int(self.data[row][col]) + 12
                    sprite = self.get_image(x, y)
                    rotval = int(self.rotdata[row][col])
                    sprite = self.rotate(sprite, rotval)
                    background.blit(sprite, (col * TILEWIDTH, row * TILEHEIGHT))
                elif self.data[row][col] == '=':
                    sprite = self.get_image(10, 8)
                    background.blit(sprite, (col * TILEWIDTH, row * TILEHEIGHT))

        return background

    # Rotates a tile image by 90-degree increments
    def rotate(self, sprite, value):
        return pygame.transform.rotate(sprite, value * 90)
