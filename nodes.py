import pygame
from vector import Vector2
from constants import *


# Represents a single intersection or junction in the maze.
# Each node can connect to neighbors in UP, DOWN, LEFT, or RIGHT directions.
class Node(object):
    def __init__(self, x, y):
        # Position of the node on the screen (in pixels)
        self.position = Vector2(x, y)

        # Dictionary of neighboring nodes, one for each direction
        self.neighbors = {
            UP: None,
            DOWN: None,
            LEFT: None,
            RIGHT: None
        }

    # Draws the node and lines to its connected neighbors.
    # WILL BE REPLACED LATER
    def render(self, screen):
        for direction in self.neighbors.keys():
            if self.neighbors[direction] is not None:
                line_start = self.position.as_tuple()
                line_end = self.neighbors[direction].position.as_tuple()

                # Draw a line from this node to the neighbor
                pygame.draw.line(screen, WHITE, line_start, line_end, 4)

                # Draw the node as a red circle
                pygame.draw.circle(screen, RED, self.position.as_int(), 12)


# A collection of all nodes in the maze.
# Handles creation and rendering of the maze's path network.
class NodeGroup(object):
    def __init__(self):
        self.nodeList = []

    # Creates a simple hardcoded test layout of nodes and their connections.
    # WILL BE REPLACED LATER
    def setup_test_nodes(self):
        # Create nodes at specific coordinates
        nodeA = Node(80 ,80)
        nodeB = Node(160, 80)
        nodeC = Node(80, 160)
        nodeD = Node(160, 160)
        nodeE = Node(208, 160)
        nodeF = Node(80, 320)
        nodeG = Node(208, 320)

        # Manually define neighbor connections between nodes
        nodeA.neighbors[RIGHT] = nodeB
        nodeA.neighbors[DOWN] = nodeC

        nodeB.neighbors[LEFT] = nodeA
        nodeB.neighbors[DOWN] = nodeD

        nodeC.neighbors[UP] = nodeA
        nodeC.neighbors[RIGHT] = nodeD
        nodeC.neighbors[DOWN] = nodeF

        nodeD.neighbors[UP] = nodeB
        nodeD.neighbors[LEFT] = nodeC
        nodeD.neighbors[RIGHT] = nodeE

        nodeE.neighbors[LEFT] = nodeD
        nodeE.neighbors[DOWN] = nodeG

        nodeF.neighbors[UP] = nodeC
        nodeF.neighbors[RIGHT] = nodeG

        nodeG.neighbors[UP] = nodeE
        nodeG.neighbors[LEFT] = nodeF

        self.nodeList = [nodeA, nodeB, nodeC, nodeD, nodeE, nodeF, nodeG]

    # Draws all nodes and their connections to the screen.
    # WILL BE REPLACED LATER
    def render(self, screen):
        for node in self.nodeList:
            node.render(screen)
