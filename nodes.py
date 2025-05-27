import pygame
from vector import Vector2
from constants import *
import numpy as np


# A Node represents a point in the maze where Pac-Man or ghosts can make decisions (turns, stops, or teleport).
# Each node knows its neighboring nodes in the four directions and portals.
class Node(object):
    def __init__(self, x, y):
        # Pixel-based position of the node
        self.position = Vector2(x, y)

        # Dictionary of connections to neighboring nodes
        self.neighbors = {
            UP: None,
            DOWN: None,
            LEFT: None,
            RIGHT: None,
            PORTAL: None
        }

        # Controls which entities are allowed to move in each direction
        self.access = {
            UP: [PACMAN, BLINKY, PINKY, INKY, CLYDE, FRUIT],
            DOWN: [PACMAN, BLINKY, PINKY, INKY, CLYDE, FRUIT],
            LEFT: [PACMAN, BLINKY, PINKY, INKY, CLYDE, FRUIT],
            RIGHT: [PACMAN, BLINKY, PINKY, INKY, CLYDE, FRUIT]
        }

    # Prevent a specific entity from moving in a given direction at this node
    def deny_access(self, direction, entity):
        if entity.name in self.access[direction]:
            self.access[direction].remove(entity.name)

    # Allow a specific entity to move in a given direction at this node
    def allow_access(self, direction, entity):
        if entity.name not in self.access[direction]:
            self.access[direction].append(entity.name)

    # Renders the node and its connections for debugging.
    # WILL BE UPDATED LATER
    def render(self, screen):
        for direction in self.neighbors:
            neighbor = self.neighbors[direction]
            if neighbor:
                pygame.draw.line(screen, DARK_GRAY, self.position.as_tuple(), neighbor.position.as_tuple(), 4)
                pygame.draw.circle(screen, DARK_GRAY, self.position.as_int(), 12)


# NodeGroup builds and manages the full network of nodes for the maze.
# It reads a text file layout, creates nodes at appropriate points,
# and connects them based on horizontal and vertical paths.
class NodeGroup(object):
    def __init__(self, level):
        # Name of maze text file
        self.level = level

        # Lookup table mapping positions to Node objects
        self.nodesLUT = {}

        # Symbols that represent nodes and valid path tiles in the maze file
        self.nodeSymbols = ['+', 'P', 'n']
        self.pathSymbols = ['.', '-', '|', 'p']

        # Load the level data and initialize the node graph
        data = self.read_maze_file(level)
        self.create_node_table(data)
        self.connect_horizontally(data)
        self.connect_vertically(data)

        # Center of ghost house
        self.homekey = None

    # Reads the maze layout from a text file as a NumPy array of characters.
    def read_maze_file(self, textfile):
        return np.loadtxt(textfile, dtype='<U1')

    # Creates nodes wherever a node symbol is found in the layout.
    # Saves them in the lookup table using pixel-based keys.
    def create_node_table(self, data, xoffset=0, yoffset=0):
        for row in list(range(data.shape[0])):
            for col in list(range(data.shape[1])):
                if data[row][col] in self.nodeSymbols:
                    x, y = self.construct_key(col + xoffset, row + yoffset)
                    self.nodesLUT[(x, y)] = Node(x, y)

    # Converts grid coordinates to pixel coordinates.
    def construct_key(self, x, y):
        return x * TILEWIDTH, y * TILEHEIGHT

    # Connects nodes to their horizontal neighbors by scanning rows.
    # Only creates connections across valid path or node symbols.
    def connect_horizontally(self, data, xoffset=0, yoffset=0):
        for row in range(data.shape[0]):
            key = None
            for col in range(data.shape[1]):
                symbol = data[row][col]
                if symbol in self.nodeSymbols:
                    if key is None:
                        key = self.construct_key(col + xoffset, row + yoffset)
                    else:
                        otherkey = self.construct_key(col + xoffset, row + yoffset)
                        self.nodesLUT[key].neighbors[RIGHT] = self.nodesLUT[otherkey]
                        self.nodesLUT[otherkey].neighbors[LEFT] = self.nodesLUT[key]
                        key = otherkey
                elif symbol not in self.pathSymbols:
                    # Reset chain if path breaks
                    key = None

    # Connects nodes to their vertical neighbors by scanning columns.
    # Similar to horizontal connection logic, but transposed.
    def connect_vertically(self, data, xoffset=0, yoffset=0):
        dataT = data.transpose()
        for col in range(dataT.shape[0]):
            key = None
            for row in range(dataT.shape[1]):
                symbol = dataT[col][row]
                if symbol in self.nodeSymbols:
                    if key is None:
                        key = self.construct_key(col + xoffset, row + yoffset)
                    else:
                        otherkey = self.construct_key(col + xoffset, row + yoffset)
                        self.nodesLUT[key].neighbors[DOWN] = self.nodesLUT[otherkey]
                        self.nodesLUT[otherkey].neighbors[UP] = self.nodesLUT[key]
                        key = otherkey
                elif symbol not in self.pathSymbols:
                    # Reset chain if path breaks
                    key = None

    # Returns a node at the given pixel position, if it exists.
    def get_node_from_pixels(self, xpixel, ypixel):
        return self.nodesLUT.get((xpixel, ypixel), None)

    # Returns a node at the given grid (tile) position.
    def get_node_from_tiles(self, col, row):
        x, y = self.construct_key(col, row)
        return self.nodesLUT.get((x, y), None)

    # Returns the first node in the list.
    # Used to temporarily assign a start node for Pac-Man.
    def get_start_temp_node(self):
        return list(self.nodesLUT.values())[0]

    # Sets up bidirectional teleport connections between two portal nodes.
    def set_portal_pair(self, pair1, pair2):
        key1 = self.construct_key(*pair1)
        key2 = self.construct_key(*pair2)
        if key1 in self.nodesLUT.keys() and key2 in self.nodesLUT.keys():
            self.nodesLUT[key1].neighbors[PORTAL] = self.nodesLUT[key2]
            self.nodesLUT[key2].neighbors[PORTAL] = self.nodesLUT[key1]

    # Creates the ghost house (where ghosts start and return after being eaten)
    def create_home_nodes(self, xoffset, yoffset):
        homedata = np.array([
            ['X', 'X', '+', 'X', 'X'],
            ['X', 'X', '.', 'X', 'X'],
            ['+', 'X', '.', 'X', '+'],
            ['+', '.', '+', '.', '+'],
            ['+', 'X', 'X', 'X', '+']
        ])
        self.create_node_table(homedata, xoffset, yoffset)
        self.connect_horizontally(homedata, xoffset, yoffset)
        self.connect_vertically(homedata, xoffset, yoffset)

        # Return the center node of the ghost house
        self.homekey = self.construct_key(xoffset + 2, yoffset)
        return self.homekey

    # Connects the ghost house to the maze
    def connect_home_nodes(self, homekey, otherkey, direction):
        key = self.construct_key(*otherkey)
        self.nodesLUT[homekey].neighbors[direction] = self.nodesLUT[key]
        self.nodesLUT[key].neighbors[direction * -1] = self.nodesLUT[homekey]

    # Deny or allow access to a specific tile direction for a single entity
    def deny_access(self, col, row, direction, entity):
        node = self.get_node_from_tiles(col, row)
        if node:
            node.deny_access(direction, entity)

    def allow_access(self, col, row, direction, entity):
        node = self.get_node_from_tiles(col, row)
        if node:
            node.allow_access(direction, entity)

    # Bulk access control for multiple entities
    def deny_access_list(self, col, row, direction, entities):
        for entity in entities:
            self.deny_access(col, row, direction, entity)

    def allow_access_list(self, col, row, direction, entities):
        for entity in entities:
            self.allow_access(col, row, direction, entity)

    def deny_home_access(self, entity):
        self.nodesLUT[self.homekey].deny_access(DOWN, entity)

    # Access control specifically for the ghost house center
    def allow_home_access(self, entity):
        self.nodesLUT[self.homekey].allow_access(DOWN, entity)

    def deny_home_access_list(self, entities):
        for entity in entities:
            self.deny_home_access(entity)

    def allow_home_access_list(self, entities):
        for entity in entities:
            self.allow_home_access(entity)

    # Draws all nodes and their connections (for debugging).
    def render(self, screen):
        for node in self.nodesLUT.values():
            node.render(screen)
