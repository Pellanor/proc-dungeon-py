import unittest

import cellular_automata as ca
import world


class TestCellularAutomata(unittest.TestCase):
    def test_init(self):
        m = world.Map(8, 4)
        n = ca.init_map(m, 0.45)
        self.assertNotEqual(m.data, n.data)

    def test_mutate(self):
        m = world.Map(150, 50)
        m = ca.init_map(m, 0.45)
        print(m.draw())
        for i in range(3):
            m = ca.mutate(m, 5, 0)
            print("itr #{}".format(str(i)))
            print(m.draw())
        for ii in range(3):
            m = ca.mutate(m, 5, -1)
            print("itr #{}".format(str(3 + ii)))
            print(m.draw())
