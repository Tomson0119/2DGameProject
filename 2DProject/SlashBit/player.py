from pico2d import *
import gfw
from gobj import *
from collision_check import *

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
        self.jump_speed = 16
        self.left_pressed = False
        self.right_pressed = False

    def enter(self):
        self.time = 0
        self.anim = 0

    def exit(self):
        pass

    def handle_event(self, e):
        pair = (e.type, e.key)
        if pair == (SDL_KEYDOWN, SDLK_LEFT) and not self.left_pressed:
            self.move_delta(-1)
            self.left_pressed = True
        elif pair == (SDL_KEYDOWN, SDLK_RIGHT) and not self.right_pressed:
            self.move_delta(1)
            self.right_pressed = True
        elif pair == (SDL_KEYUP, SDLK_LEFT) and self.left_pressed:
            self.move_delta(1)
            self.left_pressed = False
        elif pair == (SDL_KEYUP, SDLK_RIGHT) and self.right_pressed:
            self.move_delta(-1)
            self.right_pressed = False

        elif pair == (SDL_KEYDOWN, SDLK_UP):
            self.move_delta(0, self.jump_speed)
        elif pair == (SDL_KEYDOWN, SDLK_DOWN):
            self.player.set_state(CrouchState)
        elif pair == (SDL_KEYDOWN, SDLK_z):
            self.player.set_state(AttackState)

    def update(self):
        self.time += gfw.delta_time

        frame = self.time * 10
        if self.player.delta[0] != 0:
            self.anim = int(frame) % 8
        else:
            self.anim = 0

        self.delta_error_fix()

        # check boundary with tiles
        check_right(self.player)
        check_left(self.player)

        move_obj(self.player, self.player.move_speed)

    def delta_error_fix(self):
        # Delta Error Fix
        dx = self.player.delta[0]
        if (dx > 0 and not self.right_pressed) or \
                (dx == 0 and self.left_pressed) or \
                (dx == 2):
            self.move_delta(-1)
        if (dx < 0 and not self.left_pressed) or \
                (dx == 0 and self.right_pressed) or \
                (dx == -2):
            self.move_delta(1)

    def move_delta(self, dx=0, dy=0):
        self.player.delta = point_add(self.player.delta, (dx, dy))

    def draw(self):
        index = 0
        if self.player.delta[0] != 0:
            index = 2
        if self.player.delta[0] < 0:
            self.player.isLeft = True
        elif self.player.delta[0] > 0:
            self.player.isLeft = False

        self.player.draw_ex(self.anim, index)


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
        self.player.handle_event_ex(e)
        if (e.type, e.key) == (SDL_KEYUP, SDLK_DOWN):
            self.player.set_state(IdleState)

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
        self.player.Attack = True

    def exit(self):
        self.player.Attack = False

    def handle_event(self, e):
        self.player.handle_event_ex(e)

    def update(self):
        self.time += gfw.delta_time

        frame = self.time * 10
        self.anim = int(frame) % 4
        if self.anim == 3:
            self.player.set_state(IdleState)

    def draw(self):
        self.player.draw_ex(self.anim, 3)


class DeathState:
    BB_RECT = (-55, -50, 35, 4)

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

    def enter(self, collision=0):
        self.time = 0
        self.anim = 0
        collision *= -3
        self.player.delta = point_add(self.player.delta, (collision, 0))

    def exit(self):
        dx, dy = self.player.delta
        dx = 0
        self.player.delta = dx, dy

    def handle_event(self, e):
        self.player.handle_event_ex(e)

    def update(self):
        self.time += gfw.delta_time
        frame = self.time * 10

        max_index = 1 if self.player.life > 0 else 4
        if self.anim < max_index:
            self.anim = int(frame) % 5

        dx, dy = self.player.delta
        dy -= 1
        if dx <= -0.1:
            dx += 0.1
        elif dx >= 0.1:
            dx -= 0.1
        else:
            dx = 0
            if self.player.life > 0:
                self.player.set_state(IdleState)

        self.player.delta = dx, dy

        move_obj(self.player, self.player.move_speed)

        check_below(self.player)
        check_left(self.player)
        check_right(self.player)
        check_above(self.player)

    def draw(self):
        self.player.draw_ex(self.anim, 5)


class FallingState:
    BB_RECT = (-31, -48, 35, 49)

    @staticmethod
    def get(player):
        if not hasattr(FallingState, 'singleton'):
            FallingState.singleton = FallingState()
            FallingState.singleton.player = player
        return FallingState.singleton

    def __init__(self):
        self.player = None
        self.time = 0
        self.anim = 3

    def enter(self):
        self.time = 0

    def exit(self):
        pass

    def handle_event(self, e):
        self.player.handle_event_ex(e)

    def update(self):
        self.time += gfw.delta_time

        dx, dy = self.player.delta
        dy -= 1
        self.player.delta = dx, dy
        move_obj(self.player, self.player.move_speed)

        # collision check with tiles
        check_below(self.player)
        check_left(self.player)
        check_right(self.player)
        check_above(self.player)

        if check_below(self.player):
            self.player.set_state(IdleState)

    def draw(self):
        self.player.draw_ex(self.anim, 4)


class Player:
    def __init__(self):
        self.image = gfw.image.load(res(CH_DIR + 'soldier_animation_sheet.png'))
        self.state = None
        self.set_state(IdleState)
        self.pos = 200, 200
        self.delta = 0, 0
        self.move_speed = 6
        self.size = 72
        self.isLeft = False
        self.life = 5
        self.tile_bound = 0, -100, -100, -100
        self.strength = 1
        self.Attack = False
        self.attacked = False

    def set_state(self, clazz):
        if self.state is not None:
            self.state.exit()
        self.state = clazz.get(self)
        self.state.enter()

    def handle_event(self, e):
        self.state.handle_event(e)

    def handle_event_ex(self, e):
        pair = (e.type, e.key)

        state = IdleState.get(self)
        if pair == (SDL_KEYUP, SDLK_RIGHT):
            state.right_pressed = False
        elif pair == (SDL_KEYUP, SDLK_LEFT):
            state.left_pressed = False

        if pair == (SDL_KEYDOWN, SDLK_LEFT):
            state.left_pressed = True
        elif pair == (SDL_KEYDOWN, SDLK_RIGHT):
            state.right_pressed = True

    def update(self):
        self.state.update()

        left, foot, right, _ = self.get_bb()
        self.tile_bound = get_collision_bound(self.pos)
        if foot > self.tile_bound[3]:
            if self.life > 0:
                self.set_state(FallingState)

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
        left, bottom, right, top = self.state.BB_RECT
        if self.isLeft:
            left *= -1
            right *= -1
            left, right = right, left
        bb = x + left, y + bottom, x + right, y + top
        return bb

    def set_attacked(self, value, collision=0):
        self.attacked = value
        if not value:
            return
        self.set_state(DeathState)
        self.state.enter(collision)

    def stepped_on(self):
        self.delta = point_add(self.delta, (0, 20))

    def increase_life(self):
        if self.life < 10:
            self.life += 1

    def decrease_life(self, death=False):
        if self.life > 0:
            if death:
                self.life = 0
            else:
                self.life -= 1

    def increase_strength(self):
        if self.strength < 5:
            self.strength += 1

    def increase_speed(self):
        if self.move_speed < 10:
            self.move_speed += 1


