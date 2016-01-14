import itertools

import world
from tiles import tile
import my_noise as mn


class FoodTile(tile.Tile):
    def __init__(self):
        self.val = '#'
        self.colour = (0.0, 1.0, 0.0, 0.0)
        self.draw_me = True
        self.is_wall = True


class MoneyTile(tile.Tile):
    def __init__(self):
        self.val = '$'
        self.colour = (0.0, 0.0, 1.0, 0.0)
        self.draw_me = True
        self.is_wall = True


def add_resources(the_map: world.Map, food_threshold=0.85, money_threshold=0.15):
    for x, y in itertools.product(range(the_map.width), range(the_map.height)):
        if the_map.get(x, y).is_wall:
            the_noise = mn.simplex_noise_2d(x, y)
            if the_noise > food_threshold:
                the_map.set(FoodTile(), x, y, 0)
            elif the_noise < money_threshold:
                the_map.set(MoneyTile(), x, y, 0)
    return the_map
