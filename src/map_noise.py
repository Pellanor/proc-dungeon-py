import copy
import itertools
import numpy

import world
import my_noise as mn
from tiles import crevasse, tile


class RadialNoiseMap(world.Map):
    def __init__(self, width, height, depth=1, seed=0):
        super().__init__(width, height, depth, seed)
        self.data = [[[tile.Wall() for z in range(depth)] for y in range(height)] for x in range(width)]

    def add_noise(self, branches=128):
        numpy.random.seed(self.seed)
        rnd = iter(numpy.random.randint(0, 1000, branches))
        offset = 0
        offset_adjust = branches / 2 / numpy.pi
        for n in rnd:
            x = self.width / 2
            y = self.height / 2
            for i in range(self.width):
                the_noise = mn.simplex_noise_2d(n, i, self.seed) * 2 * numpy.pi + offset
                x += numpy.sin(the_noise)
                y += numpy.cos(the_noise)
                if 0 < x < self.width and 0 < y < self.height:
                    self.set(crevasse.CrevasseTile(), int(x), int(y))
            offset += offset_adjust
        return self


class RadialColourNoiseMap(world.Map):
    def __init__(self, width, height, depth=1, seed=0):
        super().__init__(width, height, depth, seed)
        self.data = [[[tile.Wall() for z in range(depth)] for y in range(height)] for x in range(width)]

    def add_noise(self, branches=360):
        numpy.random.seed(self.seed)
        rnd = iter(numpy.random.randint(0, 1000, branches))
        offset = 0
        offset_adjust = branches / 2 / numpy.pi
        for n in rnd:
            x = self.width / 2
            y = self.height / 2
            for i in range(self.width):
                the_noise = mn.simplex_noise_2d(n, i, self.seed) * 2 * numpy.pi + offset
                x += numpy.sin(the_noise)
                y += numpy.cos(the_noise)
                if 0 < x < self.width and 0 < y < self.height:
                    self.get(int(x), int(y)).colour[0] += 0.3
            offset += offset_adjust
        return self


class LinearNoiseMap(world.Map):
    def __init__(self, width, height, depth=1, seed=0):
        super().__init__(width, height, depth, seed)
        self.data = [[[tile.Wall() for z in range(depth)] for y in range(height)] for x in range(width)]

    def add_noise(self, branches=32):
        numpy.random.seed(self.seed)
        rnd = iter(numpy.random.randint(0, 1000, branches))
        for n in rnd:
            x = 0
            y = self.height / 2
            for i in range(self.width * 2):
                the_noise = mn.simplex_noise_2d(x, y, self.seed) * numpy.pi
                x -= numpy.cos(the_noise) / 2
                y += numpy.sin(the_noise) * 2
                if 0 < x < self.width and 0 < y < self.height:
                    self.set(crevasse.CrevasseTile(), int(x), int(y))
        return self


class NoiseMap(world.Map):
    def __init__(self, width, height, depth=1, seed=0):
        super().__init__(width, height, depth, seed)
        self.data = [[[tile.Wall() for z in range(depth)] for y in range(height)] for x in range(width)]

    def add_noise(self):
        for x, y in itertools.product(range(self.width), range(self.height)):
            if self.get(x, y).is_wall:
                # the_noise = (noise.snoise2(x, y, 10) + 1) / 2
                # the_noise = numpy.random.uniform()
                the_noise = mn.simplex_noise_2d(x, y)
                self.get(int(x), int(y)).colour = (the_noise, the_noise, the_noise, 0)
        return self
