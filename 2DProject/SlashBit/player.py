from pico2d import *
import gfw
from gobj import *

CH_DIR = 'character/'


class Player:
    IDLE, CROUCH, WALK, ATTACK, JUMP, DEATH = range(6)
    ANIM_INDEX = [1, 2, 8, 3, 4, 5]

    KEY_MAP = {
        (SDL_KEYDOWN, SDLK_LEFT): (-1, 0),
        (SDL_KEYDOWN, SDLK_RIGHT): (1, 0),
        (SDL_KEYDOWN, SDLK_UP): (0, 1),
        (SDL_KEYDOWN, SDLK_DOWN): (0, -1),
        (SDL_KEYUP, SDLK_LEFT): (1, 0),
        (SDL_KEYUP, SDLK_RIGHT): (-1, 0),
        (SDL_KEYUP, SDLK_UP): (0, -1),
        (SDL_KEYUP, SDLK_DOWN): (0, 1)
    }

    def __init__(self):
        self.pos = gfw.WINDOW_WIDTH // 2, gfw.WINDOW_HEIGHT // 2 - 200
        self.delta = 0, 0
        self.speed = 200
        self.image = gfw.image.load(res(CH_DIR + 'soldier_animation_sheet.png'))
        self.anim = 0
        self.left = False
        self.state = Player.IDLE
        self.jump_speed = 0

    def update_state(self):
        if self.state == Player.IDLE:
            self.state = Player.WALK
        elif self.state == Player.WALK:
            self.state = Player.IDLE


    def update_delta(self, ddx, ddy):
        dx, dy = self.delta
        dx += ddx
        self.update_state()
        self.delta = dx, dy

    def handle_event(self, e):
        pair = (e.type, e.key)
        if pair in Player.KEY_MAP:
            self.update_delta(*Player.KEY_MAP[pair])
            print("Key is being pressed")
        if pair == (SDL_KEYDOWN, SDLK_UP):
            self.jump_speed = 500
            self.state = Player.JUMP

    def update(self):
        x, y = self.pos
        dx, dy = self.delta

        if self.state == Player.JUMP:
            self.pos = point_add(self.pos, (x, self.jump_speed * gfw.delta_time))
            self.jump_speed -= 500 * gfw.delta_time
            if self.anim < Player.ANIM_INDEX[self.state] - 1:
                self.anim = (self.anim + 1) % Player.ANIM_INDEX[self.state]

            y = self.pos[1]
            if y < 100:
                y = 100
                self.state = Player.IDLE

        elif self.state == Player.WALK:
            x += dx * self.speed * gfw.delta_time
            self.anim = (self.anim + 1) % Player.ANIM_INDEX[self.state]

        # This is going to be Crouch or attack or idle
        else:
            self.anim = (self.anim + 1) % Player.ANIM_INDEX[self.state]

        self.pos = x, y

    def draw(self):
        width, height = 72, 72
        sx = self.anim * width
        sy = self.state * height

        dx = self.delta[0]
        if dx < 0:
            self.left = True
        elif dx > 0:
            self.left = False

        if self.left:
            self.image.clip_composite_draw(sx, sy, width, height, 0, 'h', *self.pos, 216, 216)
        else:
            self.image.clip_draw(sx, sy, width, height, *self.pos, 216, 216)
