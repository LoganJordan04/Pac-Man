import pygame
from vector import Vector2
from constants import *
import numpy as np


# Represents a single standard pellet in the maze.
# Pac-Man collects these for points.
class Pellet(object):
    def __init__(self, row, column):
        self.name = PELLET

        # Pixel position based on tile location
        self.position = Vector2(column * TILEWIDTH, row * TILEHEIGHT)
        self.color = WHITE

        # Visual size and collision range
        self.radius = int(2 * TILEWIDTH / 16)
        self.collideRadius = int(2 * TILEWIDTH / 16)

        # Score value
        self.points = 10

        # Toggle for rendering
        self.visible = True

    # Draws the pellet as a small white circle on the screen.
    # Only renders if pellet is marked visible.
    def render(self, screen):
        if self.visible:
            adjust = Vector2(TILEWIDTH, TILEHEIGHT) / 2
            p = self.position + adjust
            pygame.draw.circle(screen, self.color, p.as_int(), self.radius)


# A subclass of Pellet that represents a Power Pellet.
# These flash on/off and grant Pac-Man temporary power over ghosts.
class PowerPellet(Pellet):
    def __init__(self, row, column):
        Pellet.__init__(self, row, column)
        self.name = POWERPELLET

        # Larger than standard pellet
        self.radius = int(8 * TILEWIDTH / 16)

        # More points than regular pellet
        self.points = 50

        # Time between flashes in seconds
        self.flashTime = 0.2

        # Internal timer
        self.timer = 0

    # Handles flashing animation by toggling visibility on a timer.
    # Called every frame with the time delta.
    def update(self, dt):
        self.timer += dt
        if self.timer >= self.flashTime:
            self.visible = not self.visible
            self.timer = 0


# Manages a collection of regular and power pellets.
# Loads layout from a text file and handles rendering and updates.
class PelletGroup(object):
    def __init__(self, pelletfile):
        self.pelletList = []
        self.powerpellets = []
        self.create_pellet_list(pelletfile)
        self.numEaten = 0

    # Updates only power pellets (for flash animation).
    def update(self, dt):
        for powerpellet in self.powerpellets:
            powerpellet.update(dt)

    # Reads maze layout and places pellets at marked positions.
    # Symbols:
    #   '.' or '+' -> standard pellet
    #   'P' or 'p' -> power pellet
    def create_pellet_list(self, pelletfile):
        data = self.read_pelletfile(pelletfile)
        for row in range(data.shape[0]):
            for col in range(data.shape[1]):
                if data[row][col] in ['.', '+']:
                    self.pelletList.append(Pellet(row, col))
                elif data[row][col] in ['P', 'p']:
                    pp = PowerPellet(row, col)
                    self.pelletList.append(pp)
                    self.powerpellets.append(pp)

    # Loads the maze layout from a text file as a 2D NumPy array.
    def read_pelletfile(self, textfile):
        return np.loadtxt(textfile, dtype='<U1')

    # Returns True if all pellets have been eaten.
    # Used to check for level completion.
    def is_empty(self):
        return len(self.pelletList) == 0

    # Renders all visible pellets to the screen.
    def render(self, screen):
        for pellet in self.pelletList:
            pellet.render(screen)
