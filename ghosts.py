import pygame
from pygame.locals import *
from vector import Vector2
from constants import *
from entity import Entity

class Ghost(Entity):
    def __init__(self, node):
        Entity.__init__(self, node)
        self.name = GHOST
        self.points = 200

        self.goal = Vector2()

        self.directionMethod = self.goal_direction

    def goal_direction(self, directions):
        distances = []
        for direction in directions:
            vec = self.node.position + self.directions[direction] * TILEWIDTH - self.goal
            distances.append(vec.magnitude_squared())
        index = distances.index(min(distances))
        return directions[index]