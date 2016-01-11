import unittest

import noise

import world
from tiles import crevasse, resource, fort


class TestCrevasse(unittest.TestCase):

    def test_noise(self):
        for i in range(10):
            print(noise.snoise2(i, 5))

    def test_make_crevasse(self):
        for i in range(1):
            crevasse.seed = i
            print(fort.add_forts(resource.add_resources(crevasse.make_crevasse(world.Map(101, 50)))).draw())
