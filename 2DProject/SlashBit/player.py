from pico2d import *
import gfw
from gobj import *

CH_DIR = 'character/'


class Player:
    KEY_MAP = {
        (SDL_KEYDOWN, SDLK_LEFT): (-1, 0),
        (SDL_KEYDOWN, SDLK_RIGHT): (1, 0),
        (SDL_KEYUP, SDLK_LEFT): (1, 0),
        (SDL_KEYUP, SDLK_RIGHT): (-1, 0),
    }

    def __init__(self):
        self.pos = gfw.WINDOW_WIDTH // 2, gfw.WINDOW_HEIGHT // 2
        self.delta = 0, 0
        self.speed = 200
        self.image = gfw.image.load(res(CH_DIR + 'soldier_animation_sheet.png'))
        self.time = 0
        self.mag = 1
        self.anim = 0
        self.action = 0

    def update_delta(self, ddx, ddy):
        dx, dy = self.delta
        dx += ddx
        dy += ddy
        self.delta = dx, dy


    def handle_event(self, e):
        pair = (e.type, e.key)
        if pair in Player.KEY_MAP:
            self.update_delta(*Player.KEY_MAP[pair])

    def update(self):
        x, y = self.pos
        dx, dy = self.delta
        self.pos = x + dx, y + dy
       # self.anim = (self.anim + 1) % 8

    def draw(self):
        width, height = 72, 72
        sx = self.anim * width
        sy = self.action * height
        self.image.clip_composite_draw(sx, sy, width, height, 0, 'h', *self.pos, 216, 216)
        #self.image.clip_draw(sx, sy, width, height, *self.pos, 216, 216)
