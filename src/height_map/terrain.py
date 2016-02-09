import itertools

import my_noise as mn


class HeightMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.data = [[0.0 for y in range(height)] for x in range(width)]

    def get(self, x, y) -> float:
        return self.data[x][y]

    def set(self, x, y, height: float):
        self.data[x][y] = height


def make_noise_height_map(width, height, seed, octaves):
    hm = HeightMap(width, height)
    for x, y in itertools.product(range(hm.width), range(hm.height)):
        hm.set(x, y, mn.simplex_noise_2d(x, y, seed, octaves))
    return hm


def make_rising_height(width, height, seed):
    hm = HeightMap(width, height)
    for x, y in itertools.product(range(hm.width), range(hm.height)):
        hm.set(x, y, x * y / (width * height))
    return hm
