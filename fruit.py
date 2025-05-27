import pygame
from entity import Entity
from constants import *

# Represents the bonus fruit that appears temporarily in the maze.
# Inherits basic position and rendering logic from Entity.
class Fruit(Entity):
    def __init__(self, node):
        Entity.__init__(self, node)
        self.name = FRUIT

        # Color used to draw the fruit
        # WILL BE REPLACED LATER
        self.color = GREEN

        # Seconds the fruit remains active on screen
        self.lifespan = 10
        self.timer = 0

        # Flag indicating if the fruit should disappear
        self.destroy = False

        self.points = 100

        # By default, the fruit is placed in-between nodes, typically at an intersection
        self.set_between_nodes(RIGHT)

    # Updates the fruit's internal timer each frame.
    # If its lifespan expires, it sets itself to be removed from the game.
    def update(self, dt):
        self.timer += dt
        if self.timer >= self.lifespan:
            # Mark fruit for removal after time expires
            self.destroy = True
