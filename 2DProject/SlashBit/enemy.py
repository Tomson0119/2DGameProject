from pico2d import *
import gfw
from gobj import *
from collision_check import *
from random import *

CH_DIR = 'enemy/'


class IdleState:
    BB_RECT = (-36, -50, 29, 40)

    def __init__(self, Enemy):
        self.enemy = Enemy
        self.time = 0
        self.anim = 0
        self.left_pressed = False
        self.right_pressed = False

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
        if self.enemy.delta[0] != 0:
            self.anim = int(frame) % 8
        else:
            self.anim = 0

        self.update_delta()

        # check boundary with tiles
        check_left(self.enemy)
        check_right(self.enemy)

        move_obj(self.enemy, self.enemy.move_speed)

    def update_delta(self):
        rand_number = randint(1, 40)
        dx, dy = self.enemy.delta
        if rand_number == 1:
            value = randint(-1, 1)
            dx = value

        self.enemy.delta = dx, dy

    def draw(self):
        index = 0
        if self.enemy.delta[0] != 0:
            index = 1
        if self.enemy.delta[0] < 0:
            self.enemy.isLeft = True
        elif self.enemy.delta[0] > 0:
            self.enemy.isLeft = False

        self.enemy.draw_ex(self.anim, index)


class DeathState:
    BB_RECT = (-40, -50, 25, 35)

    def __init__(self, Enemy):
        self.enemy = Enemy
        self.time = 0
        self.anim = 0

    def enter(self, collision=0):
        self.time = 0
        self.anim = 0

        if abs(collision) == 2:
            collision = collision // 2
        if collision == 1:
            self.enemy.isLeft = True
        elif collision == -1:
            self.enemy.isLeft = False
        dx, dy = self.enemy.delta
        dx = 0
        self.enemy.delta = dx, dy
        self.enemy.delta = point_add(self.enemy.delta, (collision, 0))

    def exit(self):
        pass

    def handle_event(self, e):
        pass

    def update(self):
        self.time += gfw.delta_time
        frame = self.time * 10

        index_max = 1 if self.enemy.life > 0 else 4
        if self.anim < index_max:
            self.anim = int(frame) % 5

        dx, dy = self.enemy.delta
        if self.enemy.life <= 0:
            dy -= 1
        if dx < -0.1:
            dx += 0.1
        elif dx > 0.1:
            dx -= 0.1
        else:
            dx = 0
            if self.enemy.life > 0:
                self.enemy.set_state(self.enemy.idle)

        self.enemy.delta = dx, dy
        move_obj(self.enemy, self.enemy.move_speed)

        check_left(self.enemy)
        check_right(self.enemy)

    def draw(self):
        self.enemy.draw_ex(self.anim, 3)


class FallingState:
    BB_RECT = (-33, -46, 31, 45)

    def __init__(self, Enemy):
        self.enemy = Enemy
        self.time = 0
        self.anim = 0

    def enter(self):
        self.time = 0

    def exit(self):
        pass

    def handle_event(self, e):
        pass

    def update(self):
        self.time += gfw.delta_time

        dx, dy = self.enemy.delta
        dy -= 1
        self.enemy.delta = dx, dy
        move_obj(self.enemy, self.enemy.move_speed)

        # collision check with tiles
        check_below(self.enemy)

        if check_below(self.enemy):
            self.enemy.set_state(self.enemy.idle)

    def draw(self):
        self.enemy.draw_ex(self.anim, 2)


class Goblin:
    def __init__(self, x, y):
        self.image = gfw.image.load(res(CH_DIR + 'goblin_animation_sheet.png'))
        self.idle = IdleState(self)
        self.fall = FallingState(self)
        self.death = DeathState(self)
        self.state = self.idle
        self.pos = x, y
        self.delta = 0, 0
        self.move_speed = 6
        self.size = 64
        self.isLeft = False
        self.life = 3
        self.tile_bound = -100, -100, -100, -100
        self.strength = 1
        self.attacked = False
        self.active = False

    def set_state(self, clazz):
        if self.state is not None:
            self.state.exit()
        self.state = clazz
        self.state.enter()

    def handle_event(self, e):
        pass

    def update(self):
        if not self.active:
            return

        self.state.update()

        left, foot, right, _ = self.get_bb()
        self.tile_bound = get_collision_bound(self.pos)
        if foot > self.tile_bound[3]:
            if self.life > 0:
                self.set_state(self.fall)

        if self.pos[1] < 0:
            gfw.world.remove(self)

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

    def decrease_life(self, value):
        if self.life < 10:
            self.life -= value

    def set_attacked(self, value, collision=0):
        self.attacked = value
        if not value:
            return
        self.set_state(self.death)
        self.state.enter(collision)

    def move(self, dx):
        x, y = self.pos
        x += dx
        self.pos = x, y
        if x < -self.size:
            gfw.world.remove(self)

    def activate(self):
        self.active = True


class Dragon(Goblin):
    IDLE, FLY, DEATH = range(3)
    BB_RECT = [
        (-85, -70, 66, 72),
        (-86, -70, 110, 68),
        (-88, -80, 110, -20)
    ]

    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = gfw.image.load(res(CH_DIR + 'dragon_animation_sheet.png'))
        self.life = 9
        self.strength = 2
        self.size = 80

    def get_bb(self):
        index = 0
        if self.state in [self.idle, self.fall]:
            if self.delta[0] != 0:
                index = Dragon.FLY
            else:
                index = Dragon.IDLE
        elif self.state == self.death:
            index = Dragon.DEATH
        left, bottom, right, top = Dragon.BB_RECT[index]
        x, y = self.pos

        if self.isLeft:
            left *= -1
            right *= -1
            left, right = right, left
        bb = x + left, y + bottom, x + right, y + top
        return bb
