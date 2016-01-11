import unittest

import world


class TestMap(unittest.TestCase):

    def test_draw(self):
        m = world.Map(8, 4)
        print(m.draw())
