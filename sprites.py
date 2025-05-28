import pygame
from constants import *
import numpy as np
from animation import Animator

# Base dimensions of a tile in the spritesheet (used for scaling to screen resolution)
BASETILEWIDTH = 16
BASETILEHEIGHT = 16


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
        return Spritesheet.get_image(self, x, y, 2*TILEWIDTH, 2*TILEHEIGHT)

    # Assign animations for movement in each direction
    def define_animations(self):
        self.animations[LEFT] = Animator(((8, 0), (0, 0), (0, 2), (0, 0)))
        self.animations[RIGHT] = Animator(((10, 0), (2, 0), (2, 2), (2, 0)))
        self.animations[UP] = Animator(((10, 2), (6, 0), (6, 2), (6, 0)))
        self.animations[DOWN] = Animator(((8, 2), (4, 0), (4, 2), (4, 0)))

    # Update Pac-Man's animation frame based on direction
    def update(self, dt):
        if self.entity.direction == LEFT:
            self.entity.image = self.get_image(*self.animations[LEFT].update(dt))
            self.stopimage = (8, 0)
        elif self.entity.direction == RIGHT:
            self.entity.image = self.get_image(*self.animations[RIGHT].update(dt))
            self.stopimage = (10, 0)
        elif self.entity.direction == DOWN:
            self.entity.image = self.get_image(*self.animations[DOWN].update(dt))
            self.stopimage = (8, 2)
        elif self.entity.direction == UP:
            self.entity.image = self.get_image(*self.animations[UP].update(dt))
            self.stopimage = (10, 2)
        elif self.entity.direction == STOP:
            self.entity.image = self.get_image(*self.stopimage)

    # Reset all animations to initial state
    def reset(self):
        for key in list(self.animations.keys()):
            self.animations[key].reset()


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

    # Update the ghost's animation frame based on direction
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


# Handles sprite loading for the fruit bonus item.
class FruitSprites(Spritesheet):
    def __init__(self, entity):
        super().__init__()
        self.entity = entity
        self.entity.image = self.get_start_image()

    # Loads the default fruit sprite from the sheet.
    def get_start_image(self):
        return self.get_image(16, 8)

    # Returns a specific fruit sprite from tile (x, y).
    def get_image(self, x, y):
        return super().get_image(x, y, 2 * TILEWIDTH, 2 * TILEHEIGHT)


# Displays Pac-Man lives as icons on screen.
class LifeSprites(Spritesheet):
    def __init__(self, numlives):
        Spritesheet.__init__(self)
        self.reset_lives(numlives)

    # Removes one life icon (e.g., after player dies).
    def remove_image(self):
        if len(self.images) > 0:
            self.images.pop(0)

    # Resets the life icons to the specified number.
    def reset_lives(self, numlives):
        self.images = []
        for i in range(numlives):
            self.images.append(self.get_image(0,0))

    # Loads a 2x2 tile sprite for Pac-Man's life icon.
    def get_image(self, x, y):
        return Spritesheet.get_image(self, x, y, 2*TILEWIDTH, 2*TILEHEIGHT)


class MazeSprites(Spritesheet):
    def __init__(self, mazefile, rotfile):
        Spritesheet.__init__(self)
        self.data = self.read_maze_file(mazefile)
        self.rotdata = self.read_maze_file(rotfile)

    def get_image(self, x, y):
        return Spritesheet.get_image(self, x, y, TILEWIDTH, TILEHEIGHT)

    def read_maze_file(self, mazefile):
        return np.loadtxt(mazefile, dtype='<U1')

    def construct_background(self, background, y):
        for row in list(range(self.data.shape[0])):
            for col in list(range(self.data.shape[1])):
                if self.data[row][col].isdigit():
                    x = int(self.data[row][col]) + 12
                    sprite = self.get_image(x, y)
                    rotval = int(self.rotdata[row][col])
                    sprite = self.rotate(sprite, rotval)
                    background.blit(sprite, (col*TILEWIDTH, row*TILEHEIGHT))
                elif self.data[row][col] == '=':
                    sprite = self.get_image(10, 8)
                    background.blit(sprite, (col*TILEWIDTH, row*TILEHEIGHT))

        return background

    def rotate(self, sprite, value):
        return pygame.transform.rotate(sprite, value * 90)
