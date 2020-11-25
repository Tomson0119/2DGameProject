from pico2d import *
import gfw
from gobj import *

CH_DIR = 'character/'


class IdleState:
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
        self.move_speed = 2
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
        elif pair == (SDL_KEYDOWN, SDLK_LSHIFT):
            self.player.set_state(AttackState)

    def update(self):
        self.time += gfw.delta_time

        # Delta Error Fix\
        if self.player.delta[0] > 0 and not self.right_pressed:
            self.player.delta = point_add(self.player.delta, (-1, 0))
        elif self.player.delta[0] < 0 and not self.left_pressed:
            self.player.delta = point_add(self.player.delta, (1, 0))

        move_obj(self.player, self.move_speed * 2)

        frame = self.time * 10
        if self.player.delta[0] != 0:
            self.anim = int(frame) % 8
        else:
            self.anim = 0

    def draw(self):
        width, height = 72, 72
        sx = self.anim * width
        sy = 0

        if self.player.delta[0] != 0:
            sy = 2 * height
        if self.player.delta[0] < 0:
            self.player.isLeft = True
        elif self.player.delta[0] > 0:
            self.player.isLeft = False

        if self.player.isLeft:
            self.player.image.clip_composite_draw(sx, sy, width, height, 0, 'h', *self.player.pos, 216, 216)
        else:
            self.player.image.clip_draw(sx, sy, width, height, *self.player.pos, 216, 216)


class JumpState:
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
        self.move_speed = 2
        self.jump_speed = 15

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
            dy -= 1
        else:
            y = 100
            dy = 0
            self.player.set_state(IdleState)

        self.player.pos = x, y
        self.player.delta = dx, dy

        move_obj(self.player, 4)

        frame = self.time * 20
        if self.anim < 3:
            self.anim = int(frame) % 4

    def draw(self):
        width, height = 72, 72
        sx = self.anim * width
        sy = 4 * height

        if self.player.isLeft:
            self.player.image.clip_composite_draw(sx, sy, width, height, 0, 'h', *self.player.pos, 216, 216)
        else:
            self.player.image.clip_draw(sx, sy, width, height, *self.player.pos, 216, 216)


class CrouchState:
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

    def update(self):
        self.time += gfw.delta_time

        frame = self.time * 10
        if self.anim < 1:
            self.anim = int(frame) % 2

    def draw(self):
        width, height = 72, 72
        sx = self.anim * width
        sy = 1 * height

        if self.player.isLeft:
            self.player.image.clip_composite_draw(sx, sy, width, height, 0, 'h', *self.player.pos, 216, 216)
        else:
            self.player.image.clip_draw(sx, sy, width, height, *self.player.pos, 216, 216)


class AttackState:
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

        if self.anim < 2:
            frame = self.time * 10
            self.anim = int(frame) % 3
        else:
            self.player.set_state(IdleState)

    def draw(self):
        width, height = 72, 72
        sx = self.anim * width
        sy = 3 * height

        if self.player.isLeft:
            self.player.image.clip_composite_draw(sx, sy, width, height, 0, 'h', *self.player.pos, 216, 216)
        else:
            self.player.image.clip_draw(sx, sy, width, height, *self.player.pos, 216, 216)


class DeathState:
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
        width, height = 72, 72
        sx = self.anim * width
        sy = 5 * height

        if self.player.isLeft:
            self.player.image.clip_composite_draw(sx, sy, width, height, 0, 'h', *self.player.pos, 216, 216)
        else:
            self.player.image.clip_draw(sx, sy, width, height, *self.player.pos, 216, 216)


class Player:
    def __init__(self):
        self.image = gfw.image.load(res(CH_DIR + 'soldier_animation_sheet.png'))
        self.state = None
        self.set_state(IdleState)
        self.pos = 100, 100
        self.delta = 0, 0
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
