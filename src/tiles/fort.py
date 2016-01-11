import itertools

import world
from tiles import tile
from tiles import resource


class FortTile(tile.Tile):
    def __init__(self):
        self.val = '^'
        self.colour = (1.0, 0.0, 0.0, 0.0)
        self.draw_me = True
        self.is_wall = False


def add_forts(the_map: world.Map, food_range=4, money_range=4, fort_range=6):
    max_range = max(food_range, money_range, fort_range)
    for x, y in itertools.product(range(the_map.width), range(the_map.height)):
        if not the_map.get(x, y).is_wall:
            food = 0
            money = 0
            fort = 0
            for ox, oy in itertools.product(get_safe_range(x, the_map.width, max_range),
                                            get_safe_range(y, the_map.height, max_range)):
                if max(abs(ox - x), abs(oy - y)) <= food_range and \
                        isinstance(the_map.get(ox, oy), resource.FoodTile().__class__):
                    food += 1
                if max(abs(ox - x), abs(oy - y)) <= money_range and \
                        isinstance(the_map.get(ox, oy), resource.MoneyTile().__class__):
                    money += 1
                if max(abs(ox - x), abs(oy - y)) <= fort_range and \
                        isinstance(the_map.get(ox, oy), FortTile().__class__):
                    fort += 1
            if not fort and money > 2 and food > 2 and food + money > 5:
                the_map.set(FortTile(), x, y, 0)

    return the_map


def get_safe_range(val, upper_bound, offset=3):
    start = max(0, val - offset)
    stop = min(upper_bound - 1, val + offset)
    return range(start, stop + 1)
