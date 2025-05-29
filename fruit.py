import pygame
from entity import Entity
from constants import *
from sprites import FruitSprites

# Represents the bonus fruit that appears temporarily in the maze.
# Inherits basic position and rendering logic from Entity.
class Fruit(Entity):
    def __init__(self, node, level=0):
        Entity.__init__(self, node)
        self.name = FRUIT

        # Color used if rendering as a shape instead of sprite
        self.color = GREEN

        # Loads fruit sprite graphic
        self.sprites = FruitSprites(self, level)

        # Seconds the fruit remains active on screen
        self.lifespan = 10
        self.timer = 0

        # Flag indicating if the fruit should disappear
        self.destroy = False

        # Score points based on level progression
        self.points = 100 + level*20

        # By default, the fruit is placed in-between nodes, typically at an intersection
        self.set_between_nodes(RIGHT)

    # Updates the fruit's internal timer each frame.
    # If its lifespan expires, it sets itself to be removed from the game.
    def update(self, dt):
        self.timer += dt
        if self.timer >= self.lifespan:
            # Mark fruit for removal after time expires
            self.destroy = True
