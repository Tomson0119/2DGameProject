import gfw
from pico2d import *

RES_DIR = 'res/'


def res(name):
    return RES_DIR + name


def point_add(point1, point2, speed_x=1, speed_y=1):
    x1, y1 = point1
    x2, y2 = point2
    return x1 + x2 * speed_x, y1 + y2 * speed_y


def move_obj(obj, speed_x=1, speed_y=1):
    obj.pos = point_add(obj.pos, obj.delta, speed_x, speed_y)


class ImageObject:
    def __init__(self, name, pos):
        self.image = gfw.image.load(RES_DIR + name)
        self.pos = pos

    def draw(self):
        self.image.draw(*self.pos, gfw.WINDOW_WIDTH, gfw.WINDOW_HEIGHT)

    def update(self):
        pass
