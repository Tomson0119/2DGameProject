import gfw
import gobj
from pico2d import *

CH_DIR = 'character/'


class Character:
    def __init__(self, x, y, imageName):
        self.image = gfw.image.load(gobj.res(CH_DIR + imageName))
        self.size = 72
        self.anim = 0
        self.index = 0
        self.pos = x, y
        self.time = 0
        self.max_anim = 1
        self.mag = 5

    def update(self):
        self.time += gfw.delta_time
        frame = self.time * 10
        self.anim = int(frame) % self.max_anim

    def draw(self):
        sx = self.anim * self.size
        sy = self.index * self.size
        size = self.size, self.size
        draw_size = self.size * self.mag, self.size * self.mag
        self.image.clip_draw(sx, sy, *size, *self.pos, *draw_size)

    def set_animation(self, value):
        if value:
            self.max_anim = 8
            self.index = 2
        else:
            self.max_anim = 1
            self.index = 0
