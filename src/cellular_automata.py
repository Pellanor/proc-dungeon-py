import copy
import itertools

import numpy

import world
from tiles import crevasse, tile


class CAMap(world.Map):
    def __init__(self, width, height, depth=1, seed=0):
        super().__init__(width, height, depth, seed)
        self.data = [[[tile.Wall() for z in range(depth)] for y in range(height)] for x in range(width)]

    def init(self, fill_percent: float):
        numpy.random.seed(self.seed)
        for x, y in itertools.product(range(1, self.width - 1), range(1, self.height - 1)):
            if numpy.random.uniform() > fill_percent:
                self.set(crevasse.CrevasseTile(), x, y)
        return self

    def mutate(self, max_walls=5, min_walls=-1, make_wall=True, iterations=1):
        old_map = self
        new_map = self
        for i in range(iterations):
            new_map = copy_ca_map(old_map)
            for x, y in itertools.product(range(1, old_map.width - 1), range(1, old_map.height - 1)):
                wall_count = 0
                for x2, y2 in itertools.product(range(x - 1, x + 2), range(y - 1, y + 2)):
                    if old_map.get(x2, y2).is_wall:
                        wall_count += 1
                if (wall_count >= max_walls or wall_count <= min_walls) and make_wall:
                    new_map.set(tile.Wall(), x, y)
                else:
                    new_map.set(crevasse.CrevasseTile(), x, y)
            old_map = new_map
        return new_map


def copy_ca_map(old_map: CAMap) -> CAMap:
    new_map = CAMap(old_map.width, old_map.height, old_map.depth, old_map.seed)
    new_map.data = copy.deepcopy(old_map.data)
    return new_map

# TODO: Find some kind of map-wide "flow" for different mystical energy sources
# TODO: Generate resources
