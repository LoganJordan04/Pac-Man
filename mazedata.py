from constants import *

# Base class defining shared maze configuration logic for all levels
class MazeBase(object):
    def __init__(self):
        self.portalPairs = {}
        self.homeoffset = (0, 0)
        self.ghostNodeDeny = {
            UP:(), DOWN:(), LEFT:(), RIGHT:()
        }

    # Links portal node pairs in the maze.
    # Called by the controller to activate teleportation paths.
    def set_portal_pairs(self, nodes):
        for pair in list(self.portalPairs.values()):
            nodes.set_portal_pair(*pair)

    # Connects the ghost home (spawn) nodes to the rest of the graph using preset directions.
    def connect_home_nodes(self, nodes):
        key = nodes.create_home_nodes(*self.homeoffset)
        nodes.connect_home_nodes(key, self.homenodeconnectLeft, LEFT)
        nodes.connect_home_nodes(key, self.homenodeconnectRight, RIGHT)

    # Applies the homeoffset to a coordinate pair.
    # Useful for positioning ghost house entries.
    def add_offset(self, x, y):
        return x+self.homeoffset[0], y+self.homeoffset[1]

    # Restricts ghost access to specific tiles and directions.
    # Prevents them from entering invalid or game-designated areas.
    def deny_ghosts_access(self, ghosts, nodes):
        nodes.deny_access_list(*(self.add_offset(2, 3) + (LEFT, ghosts)))
        nodes.deny_access_list(*(self.add_offset(2, 3) + (RIGHT, ghosts)))

        for direction in list(self.ghostNodeDeny.keys()):
            for values in self.ghostNodeDeny[direction]:
                nodes.deny_access_list(*(values + (direction, ghosts)))


# Handles selection and instantiation of the maze based on level
class MazeData(object):
    def __init__(self):
        self.obj = None
        self.mazedict = {
            0:Maze1,
            1:Maze2
        }

    # Loads the maze for the current level.
    # Loops through available maze layouts using modulo indexing.
    def load_maze(self, level):
        self.obj = self.mazedict[level % len(self.mazedict)]()


# Maze variant 1: layout and node configuration
class Maze1(MazeBase):
    def __init__(self):
        super().__init__()
        self.name = "maze1"

        # Define linked portal pair(s)
        self.portalPairs = {0:((0, 17), (27, 17))}

        # Ghost home node offset and connection points
        self.homeoffset = (11.5, 14)
        self.homenodeconnectLeft = (12, 14)
        self.homenodeconnectRight = (15, 14)

        # Pac-Man and fruit starting positions
        self.pacmanStart = (15, 26)
        self.fruitStart = (9, 20)

        # Ghost movement restrictions
        self.ghostNodeDeny = {
            UP: ((12, 14), (15, 14), (12, 26), (15, 26)),
            LEFT: (self.add_offset(2, 3),),
            RIGHT: (self.add_offset(2, 3),)
        }


# Maze variant 2: alternate layout and configuration
class Maze2(MazeBase):
    def __init__(self):
        super().__init__()
        self.name = "maze2"

        # This maze has two pairs of portals
        self.portalPairs = {
            0: ((0, 4), (27, 4)),
            1: ((0, 26), (27, 26))
        }

        self.homeoffset = (11.5, 14)
        self.homenodeconnectLeft = (9, 14)
        self.homenodeconnectRight = (18, 14)
        self.pacmanStart = (16, 26)
        self.fruitStart = (11, 20)
        self.ghostNodeDeny = {
            UP:((9, 14), (18, 14), (11, 23), (16, 23)),
            LEFT:(self.add_offset(2, 3),),
            RIGHT:(self.add_offset(2, 3),)
        }
