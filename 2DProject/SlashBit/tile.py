from pico2d import *
import gfw
import gobj

TILE_DIR = 'tile/'

UNIT = 100


class Tile:
    def __init__(self, type, left, bottom):
        self.left = left
        self.bottom = bottom
        self.size = 96
        self.image = gfw.image.load(gobj.res(TILE_DIR + 'tiles_%03d.png' % type))

    def update(self):
        pass

    def draw(self):
        self.image.draw_to_origin(self.left, self.bottom, self.size, self.size)

    def get_bb(self):
        return self.left, self.bottom, self.left + self.size, self.bottom + self.size

    def move(self, dx):
        self.left += dx
        if self.left + self.size < 0:
            gfw.world.remove(self)

