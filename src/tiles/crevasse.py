import world
from tiles import tile
import my_noise as mn


class CrevasseTile(tile.Tile):
    def __init__(self):
        self.val = ' '
        self.colour = (0.0, 0.0, 0.0, 0.0)
        self.draw_me = False
        self.is_wall = False


def make_crevasse(the_map: world.Map):
    h = the_map.height
    w = the_map.width
    for y in range(h):
        the_noise = mn.simplex_noise_1d(y, the_map.seed) * (w / 2)  # Output from 0 to width/2
        border = (w - the_noise) / 2.0  # Space on either side of the crevice
        for x in range(w):
            if border < x < w - border:
                the_map.set(CrevasseTile(), x, y, 0)
    return the_map
