from pico2d import *
import gfw
import gobj

TILE_DIR = 'tile/'
ITEM_DIR = 'item/'
UNIT = 100


class Tile:
    def __init__(self, type, left, bottom):
        self.init(left, bottom)
        self.size = 96
        self.image = gfw.image.load(gobj.res(TILE_DIR + 'tiles_%03d.png' % type))

    def init(self, left, bottom):
        self.left = left
        self.bottom = bottom

    def update(self):
        pass

    def draw(self):
        self.image.draw_to_origin(self.left, self.bottom, self.size, self.size)

    def get_bb(self):
        return self.left, self.bottom, self.left + self.size, self.bottom + self.size

    def move(self, dx):
        self.left += dx


class Heart(Tile):
    def __init__(self, left, bottom):
        self.name = 'Heart'
        self.init(left, bottom)
        self.image = gfw.image.load(gobj.res(ITEM_DIR + 'heart.png'))
        self.size = 64


class Potion(Tile):
    def __init__(self, color, left, bottom):
        if color == 'red':
            self.name = 'RedPotion'
            self.image = gfw.image.load(gobj.res(ITEM_DIR + 'potion_red.png'))
        elif color == 'blue':
            self.name = 'BluePotion'
            self.image = gfw.image.load(gobj.res(ITEM_DIR + 'potion_blue.png'))
        self.init(left, bottom)
        self.size = 64


class Spike(Tile):
    def __init__(self, left, bottom):
        self.image = gfw.image.load(gobj.res(ITEM_DIR + 'spikes.png'))
        self.init(left, bottom)
        self.size = 96

    def get_bb(self):
        return self.left, self.bottom + 10, self.left + self.size, self.bottom + self.size // 2 - 3
