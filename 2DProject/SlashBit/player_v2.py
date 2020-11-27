from pico2d import *
import gfw
from gobj import *

CH_DIR = 'character/'


class Player:
    IDLE, CROUCH, WALK, ATTACK, JUMP, DEATH, FALL = range(7)
    ANIM = [1, 2, 8, 3, 4, 5]
    BB_RECT = [
        (-33, -48, 33, 43),  # IDLE
        (-27, -48, 39, 28),  # CROUCH
        (-33, -48, 33, 43),  # WALK
        (-27, -48, 100, 40),  # ATTACK
        (-31, -48, 35, 49),  # JUMP
        (0, 0, 0, 0),  # Death
        (-31, -48, 35, 49)  # FALL
    ]
    FPS = 10
    GRAVITY = 1

    def __init__(self):
        self.pos = 100, 200
        self.delta = 0, 0
        self.image = gfw.image.load(res(CH_DIR + 'soldier_animation_sheet.png'))
        self.move_speed = 5
        self.jump_speed = 15
        self.size = 72
        self.state = Player.IDLE
        self.isLeft = False
        self.life = 5
        self.anim = 0
        self.time = get_time()

    def walk(self, way, up=False):
        if self.state in [Player.IDLE, Player.WALK]:
            dx, dy = self.delta
            if up and dx != 0:
                return
            dx += way * self.move_speed
            self.delta = dx, dy
            if dx < 0:
                self.isLeft = True
            elif dx > 0:
                self.isLeft = False
            self.state = Player.IDLE if dx == 0 else Player.WALK

    def set_jump(self):
        if self.state in [Player.IDLE, Player.WALK]:
            self.state = Player.JUMP
            dx = self.delta[0]
            self.delta = dx, self.jump_speed

    def handle_event(self, e):
        pair = (e.type, e.key)
        if pair == (SDL_KEYDOWN, SDLK_LEFT):
            self.walk(-1)
        elif pair == (SDL_KEYDOWN, SDLK_RIGHT):
            self.walk(1)
        elif pair == (SDL_KEYUP, SDLK_LEFT):
            self.walk(1)
        elif pair == (SDL_KEYUP, SDLK_RIGHT):
            self.walk(-1)

        if pair == (SDL_KEYDOWN, SDLK_UP):
            print("jump")
            self.set_jump()

    def update(self):
        self.pos = point_add(self.pos, self.delta)
        left, foot, right, _ = self.get_bb()
        top = self.get_below_tile_top()
        if foot > top:
            self.state = Player.FALL

        if self.state == Player.FALL:
            x, y = self.pos
            dx, dy = self.delta
            dy -= self.GRAVITY
            self.delta = dx, dy

            if foot <= top:
                y = top + (y - foot)
                self.pos = x, y
                dx, dy = self.delta

                self.delta = dx, 0
                self.state = Player.IDLE

    def draw(self):
        elapsed = get_time() - self.time

        index = self.state
        if self.state == Player.FALL:
            index = Player.JUMP
        self.anim = int(elapsed * Player.FPS) % self.ANIM[index]
        if index == Player.JUMP:
            self.anim = self.ANIM[index] - 1

        sx = self.anim * self.size
        sy = index * self.size
        draw_size = self.size * 3, self.size * 3

        if self.isLeft:
            self.image.clip_composite_draw(sx, sy, self.size, self.size, 0, 'h', *self.pos, *draw_size)
        else:
            self.image.clip_draw(sx, sy, self.size, self.size, *self.pos, *draw_size)

    def get_bb(self):
        left, bottom, right, top = Player.BB_RECT[self.state]
        x, y = self.pos
        if self.isLeft:
            left *= -1
            right *= -1
        return x + left, y + bottom, x + right, y + top

    def get_below_tile_top(self):
        sel_top = -100
        x, y = self.pos
        for tile in gfw.world.objects_at(gfw.layer.tile):
            left, bottom, right, top = tile.get_bb()
            if left <= x <= right and y > top:
                if sel_top == -100:
                    sel_top = top
                else:
                    if top > sel_top:
                        sel_top = top
        return sel_top
