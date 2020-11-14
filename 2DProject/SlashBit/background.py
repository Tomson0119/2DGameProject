import gfw
from pico2d import *
from gobj import *

BG_DIR = 'background/'


class Background:
    def __init__(self, imageName):
        self.imageName = imageName
        self.image = gfw.image.load(res(BG_DIR + imageName))
        self.cw = gfw.WINDOW_WIDTH
        self.ch = gfw.WINDOW_HEIGHT
        self.rect = 0, 0, self.image.w, self.image.h

    def draw(self):
        self.image.clip_draw_to_origin(*self.rect, 0, 0, self.cw, self.ch)

    def update(self):
        pass


class HorzScrollBackground:
    def __init__(self, imageName, speed, pos_y):
        self.imageName = imageName
        self.image = gfw.image.load(res(BG_DIR + imageName))
        self.cw = gfw.WINDOW_WIDTH
        self.ch = gfw.WINDOW_HEIGHT
        self.scroll, self.speed = 0, speed
        self.pos_y = pos_y

    def draw(self):
        page = self.image.w * self.ch // self.image.h
        curr = int(-self.scroll) % page

        if curr > 0:
            sw = int(1 + self.image.h * curr / self.ch)
            sl = self.image.w - sw
            src = sl, 0, sw, self.image.h
            dw = int(sw * self.ch / self.image.h)
            dst = curr - dw, self.pos_y, dw, self.ch
            self.image.clip_draw_to_origin(*src, *dst)

        dst_width = round(self.image.w * self.ch / self.image.h)
        while curr + dst_width < self.cw:
            dst = curr, self.pos_y, dst_width, self.ch
            self.image.draw_to_origin(*dst)
            curr += dst_width

        if curr < self.cw:
            dw = self.cw - curr
            sw = int(1 + self.image.h * dw / self.ch)
            src = 0, 0, sw, self.image.h
            dw = int(sw * self.ch / self.image.h)
            dst = curr, self.pos_y, dw, self.ch
            self.image.clip_draw_to_origin(*src, *dst)

    def update(self):
        self.scroll += self.speed * gfw.delta_time