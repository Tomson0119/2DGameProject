from pico2d import *
import gfw
from gobj import *

CH_DIR = 'character/'


class IdleState:
    BB_RECT = (-33, -48, 33, 43)

    @staticmethod
    def get(player):
        if not hasattr(IdleState, 'singleton'):
            IdleState.singleton = IdleState()
            IdleState.singleton.player = player
        return IdleState.singleton

    def __init__(self):
        self.player = None
        self.time = 0
        self.anim = 0
        self.move_speed = 10
        self.left_pressed = False
        self.right_pressed = False

    def enter(self):
        self.time = 0
        self.anim = 0

    def exit(self):
        pass

    def handle_event(self, e):
        pair = (e.type, e.key)
        if pair == (SDL_KEYDOWN, SDLK_LEFT):
            self.player.delta = point_add(self.player.delta, (-1, 0))
            self.left_pressed = True
        elif pair == (SDL_KEYDOWN, SDLK_RIGHT):
            self.player.delta = point_add(self.player.delta, (1, 0))
            self.right_pressed = True
        elif pair == (SDL_KEYUP, SDLK_LEFT) and self.left_pressed:
            self.player.delta = point_add(self.player.delta, (1, 0))
            self.left_pressed = False
        elif pair == (SDL_KEYUP, SDLK_RIGHT) and self.right_pressed:
            self.player.delta = point_add(self.player.delta, (-1, 0))
            self.right_pressed = False

        elif pair == (SDL_KEYDOWN, SDLK_UP):
            self.player.set_state(JumpState)
        elif pair == (SDL_KEYDOWN, SDLK_DOWN):
            self.player.set_state(CrouchState)
        elif pair == (SDL_KEYDOWN, SDLK_z):
            self.player.set_state(AttackState)

    def update(self):
        self.time += gfw.delta_time

        # Delta Error Fix\
        if self.player.delta[0] > 0 and not self.right_pressed:
            self.player.delta = point_add(self.player.delta, (-1, 0))
        elif self.player.delta[0] < 0 and not self.left_pressed:
            self.player.delta = point_add(self.player.delta, (1, 0))

        move_obj(self.player, self.move_speed)

        frame = self.time * 10
        if self.player.delta[0] != 0:
            self.anim = int(frame) % 8
        else:
            self.anim = 0

    def draw(self):
        index = 0
        if self.player.delta[0] != 0:
            index = 2
        if self.player.delta[0] < 0:
            self.player.isLeft = True
        elif self.player.delta[0] > 0:
            self.player.isLeft = False

        self.player.draw_ex(self.anim, index)


class JumpState:
    BB_RECT = (-31, -48, 35, 49)

    @staticmethod
    def get(player):
        if not hasattr(JumpState, 'singleton'):
            JumpState.singleton = JumpState()
            JumpState.singleton.player = player
        return JumpState.singleton

    def __init__(self):
        self.player = None
        self.time = 0
        self.anim = 0
        self.jump_speed = 25

    def enter(self):
        self.time = 0
        self.anim = 0
        self.player.delta = point_add(self.player.delta, (0, self.jump_speed))

    def exit(self):
        pass

    def handle_event(self, e):
        pair = (e.type, e.key)

        state = IdleState.get(self.player)
        if pair == (SDL_KEYUP, SDLK_RIGHT):
            state.right_pressed = False
        elif pair == (SDL_KEYUP, SDLK_LEFT):
            state.left_pressed = False

    def update(self):
        self.time += gfw.delta_time

        # Decrease delta y
        x, y = self.player.pos
        dx, dy = self.player.delta
        if y >= 100:
            dy -= 2
        else:
            y = 100
            dy = 0
            self.player.set_state(IdleState)

        self.player.pos = x, y
        self.player.delta = dx, dy

        move_obj(self.player, 10)

        frame = self.time * 20
        if self.anim < 3:
            self.anim = int(frame) % 4

    def draw(self):
        self.player.draw_ex(self.anim, 4)


class CrouchState:
    BB_RECT = (-27, -48, 39, 28)

    @staticmethod
    def get(player):
        if not hasattr(CrouchState, 'singleton'):
            CrouchState.singleton = CrouchState()
            CrouchState.singleton.player = player
        return CrouchState.singleton

    def __init__(self):
        self.player = None
        self.time = 0
        self.anim = 0

    def enter(self):
        self.time = 0
        self.anim = 0

    def exit(self):
        pass

    def handle_event(self, e):
        pair = (e.type, e.key)

        if pair == (SDL_KEYUP, SDLK_DOWN):
            self.player.set_state(IdleState)

        state = IdleState.get(self.player)
        if pair == (SDL_KEYUP, SDLK_RIGHT):
            state.right_pressed = False
        elif pair == (SDL_KEYUP, SDLK_LEFT):
            state.left_pressed = False

    def update(self):
        self.time += gfw.delta_time

        frame = self.time * 10
        if self.anim < 1:
            self.anim = int(frame) % 2

    def draw(self):
        self.player.draw_ex(self.anim, 1)


class AttackState:
    BB_RECT = (-27, -48, 100, 40)

    @staticmethod
    def get(player):
        if not hasattr(AttackState, 'singleton'):
            AttackState.singleton = AttackState()
            AttackState.singleton.player = player
        return AttackState.singleton

    def __init__(self):
        self.player = None
        self.time = 0
        self.anim = 0

    def enter(self):
        self.time = 0
        self.anim = 0

    def exit(self):
        pass

    def handle_event(self, e):
        pass

    def update(self):
        self.time += gfw.delta_time

        frame = self.time * 10
        self.anim = int(frame) % 4
        if self.anim == 3:
            self.player.set_state(IdleState)

    def draw(self):
        self.player.draw_ex(self.anim, 3)


class DeathState:
    BB_RECT = (0, 0, 0, 0)

    @staticmethod
    def get(player):
        if not hasattr(DeathState, 'singleton'):
            DeathState.singleton = DeathState()
            DeathState.singleton.player = player
        return DeathState.singleton

    def __init__(self):
        self.player = None
        self.time = 0
        self.anim = 0

    def enter(self):
        self.time = 0
        self.anim = 0

        move_back = 2 if self.player.isLeft else -2
        self.player.delta = point_add(self.player.delta, (move_back, 0))

    def exit(self):
        pass

    def handle_event(self, e):
        pass

    def update(self):
        self.time += gfw.delta_time

        x, y = self.player.pos
        dx, dy = self.player.delta
        if y > 100:
            dy -= 1
        else:
            y = 100
            dy = 0
            self.player.pos = x, y
        move_obj(self.player, 4)

        if self.anim < 4:
            frame = self.time * 10
            self.anim = int(frame) % 5
        elif self.player.pos[1] <= 100:
            dx = 0
        self.player.delta = dx, dy

    def draw(self):
        self.player.draw_ex(self.anim, 5)


class Player:
    def __init__(self):
        self.image = gfw.image.load(res(CH_DIR + 'soldier_animation_sheet.png'))
        self.state = None
        self.set_state(IdleState)
        self.pos = 100, 100
        self.delta = 0, 0
        self.size = 72
        self.isLeft = False
        self.life = 5

    def set_state(self, clazz):
        if self.state is not None:
            self.state.exit()
        self.state = clazz.get(self)
        self.state.enter()

    def handle_event(self, e):
        self.state.handle_event(e)

        if (e.type, e.key) == (SDL_KEYDOWN, SDLK_y):
            self.life -= 1

    def update(self):
        self.state.update()
        if self.life == 0:
            self.life -= 1
            self.set_state(DeathState)

    def draw(self):
        self.state.draw()

    def draw_ex(self, anim, index):
        sx = anim * self.size
        sy = index * self.size

        if self.isLeft:
            self.image.clip_composite_draw(sx, sy, self.size, self.size,
                                           0, 'h', *self.pos, self.size * 3, self.size * 3)
        else:
            self.image.clip_draw(sx, sy, self.size, self.size,
                                 *self.pos, self.size * 3, self.size * 3)

    def get_bb(self):
        x, y = self.pos
        l, b, r, t = self.state.BB_RECT
        if self.isLeft:
            l *= -1
            r *= -1
        bb = x + l, y + b, x + r, y + t
        return bb
