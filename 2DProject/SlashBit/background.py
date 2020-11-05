import gfw
from pico2d import *
from gobj import *

class Background:
    def __init__(self, imageName):
        self.imageName = imageName
        self.image = gfw.image.load(res(imageName))
        self.winw = gfw.WINDOW_WIDTH
        self.winh = gfw.WINDOW_HEIGHT
        self.rect = 0, 0, self.image.w, self.image.h

    def draw(self):
        self.image.clip_draw_to_origin(*self.rect,0,0,self.winw,self.winh)

    def update(self):
        pass