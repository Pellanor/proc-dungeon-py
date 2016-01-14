class Tile:
    val = None
    colour = None
    draw_me = False
    is_wall = False

    def draw(self):
        return self.val

    def __str__(self):
        return self.draw()

    def __repr__(self):
        return self.draw()

    @property
    def empty(self):
        return self.val is None


class Wall(Tile):
    def __init__(self):
        self.val = '.'
        self.colour = [0.0, 0.0, 0.0, 0.0]
        self.draw_me = True
        self.is_wall = True
