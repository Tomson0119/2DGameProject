from pico2d import *
import gfw
import gobj


class Menu:
    def __init__(self, file, size, rgb, sentence, pos_x, pos_y):
        self.color = rgb
        self.font = gfw.font.load(gobj.res(file), size)
        self.hw, self.hh = gfw.WINDOW_WIDTH // 2, gfw.WINDOW_HEIGHT // 2
        self.pos = (self.hw + pos_x, self.hh + pos_y)
        self.sentence = sentence

    def update(self):
        pass

    def draw(self, time=None):
        if time is None:
            self.font.draw(*self.pos, self.sentence, self.color)
        else:
            _, rem = divmod(time, 3600)
            minutes, seconds = divmod(rem, 60)
            str = self.sentence + "{:0} second".format(int(seconds))
            self.font.draw(*self.pos, str, self.color)



