import gfw
from pico2d import *

RES_DIR = 'res/'

class ImageObject:
    def __init__(self,name,pos):
        self.image = gfw.image.load(RES_DIR + name)
        self.pos = pos
    def draw(self):
        self.image.draw(*self.pos, gfw.WINDOW_WIDTH, gfw.WINDOW_HEIGHT)
    def update(self):
        pass

if __name__ == "__main__":
    print("This module should not be loaded directly")