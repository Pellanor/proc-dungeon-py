import world
from tiles import tile
import noise


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
        the_noise = (1 + noise.snoise2(the_map.seed, y, 5)) / 4.0 * w  # Output from 0 to width/2
        border = (w - the_noise) / 2.0  # Space on either side of the crevice
        for x in range(w):
            if border < x < w - border:
                the_map.set(CrevasseTile(), x, y, 0)
    return the_map
