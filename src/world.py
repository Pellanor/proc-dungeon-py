import copy

from tiles import tile


class Map:
    def __init__(self, width, height, depth=1, seed=0):
        self.width = width
        self.height = height
        self.depth = depth
        self.data = [[[tile.Tile() for z in range(depth)] for y in range(height)] for x in range(width)]
        self.seed = seed

    def get(self, x, y, z=0) -> tile.Tile:
        return self.data[x][y][z]

    def set(self, i_tile: tile.Tile, x, y, z=0):
        self.data[x][y][z] = i_tile

    def draw(self):
        output = "Map {}x{}\n".format(self.width, self.height)
        output += '\n'.join([''.join([self.get(x, y).draw() for x in range(self.width)]) for y in range(self.height)])
        return output


def copy_map(old_map: Map):
    new_map = Map(old_map.width, old_map.height, old_map.depth, old_map.seed)
    new_map.data = copy.deepcopy(old_map.data)
    return new_map
