import gfw
from pico2d import *


def collides_check(a, b):
    al, ab, ar, at = a.get_bb()
    bl, bb, br, bt = b.get_bb()

    # step on
    if bt <= ab <= bt + 10:
        if al <= bl <= ar:
            return 2
        if al <= br <= ar:
            return -2
    elif (at <= bt or ab <= bt) and \
            (at >= bb or ab >= bb):
        # player -> enemy
        if al <= bl <= ar:
            return 1
        # enemy -> player
        if al <= br <= ar:
            return -1
    return 0


def check_valid(obj):
    left, _, right, _ = obj.get_bb()
    size = obj.size
    max_size = size + get_canvas_width()
    if -size <= left <= max_size and \
            -size <= right <= max_size:
        return True
    else:
        return False


def check_collision(Player):
    for item in gfw.world.objects_at(gfw.layer.item):
        if check_valid(item):
            if collides_check(Player, item) != 0:
                if item.name == 'Heart':
                    Player.increase_life()
                if item.name == 'RedPotion':
                    Player.increase_strength()
                if item.name == 'BluePotion':
                    print("increase speed")
                    Player.increase_speed()
                if item.name == 'Key':
                    print("Game clear")
                    gfw.world.remove(item)
                    return True
                gfw.world.remove(item)

    for spike in gfw.world.objects_at(gfw.layer.spike):
        if check_valid(spike):
            if collides_check(Player, spike) != 0 and Player.life > 0:
                Player.decrease_life(death=True)
                Player.set_attacked(True, collision=0)

    for enemy in gfw.world.objects_at(gfw.layer.enemy):
        if check_valid(enemy):
            if Player.Attacking:
                collision = collides_check(Player, enemy)
                if collision != 0 and not enemy.attacked:
                    print("Attack")
                    enemy.decrease_life(Player.strength)
                    enemy.set_attacked(True, collision)
                elif not enemy.attacked:
                    collision_with_enemy(Player, enemy)
            else:
                enemy.set_attacked(False)
                collision_with_enemy(Player, enemy)
    return False


def collision_with_enemy(Player, enemy):
    collision = collides_check(Player, enemy)
    if abs(collision) == 1 and not Player.attacked:
        print("attacked")
        Player.set_attacked(True, collision)
        Player.decrease_life()
    elif abs(collision) == 2 and not enemy.attacked:
        print("stepped on")
        enemy.set_attacked(True, collision)
        enemy.decrease_life(Player.strength * 10)
        Player.stepped_on()
    else:
        Player.set_attacked(False)
        enemy.set_attacked(False)


def check_below(Player):
    _, foot, _, _ = Player.get_bb()
    dx, dy = Player.delta
    x, y = Player.pos

    if foot <= Player.tile_bound[3]:
        dy = 0
        y = Player.tile_bound[3] + (Player.pos[1] - foot)
        Player.pos = x, y
        Player.delta = dx, dy
        return True


def check_right(Player):
    _, _, right, _ = Player.get_bb()
    dx, dy = Player.delta
    if Player.tile_bound[0] < 0:
        return False

    if right >= Player.tile_bound[0]:
        if dx >= 0:
            dx = 0
        Player.delta = dx, dy
        return True


def check_left(Player):
    left, _, _, _ = Player.get_bb()
    dx, dy = Player.delta

    if left <= Player.tile_bound[2] or left <= 0:
        if dx <= 0:
            dx = 0
        Player.delta = dx, dy
        return True


def check_above(Player):
    _, _, _, head = Player.get_bb()
    x, y = Player.pos
    dx, dy = Player.delta
    if Player.tile_bound[1] < 0:
        return False

    if head >= Player.tile_bound[1]:
        dy = 0
        y = Player.tile_bound[1] - (head - Player.pos[1])
        Player.pos = x, y
        Player.delta = dx, dy
        return True


def get_collision_bound(pos):
    left = get_tile_left(pos)
    right = get_tile_right(pos)
    top = get_tile_top(pos)
    bottom = get_tile_bottom(pos)

    return left, bottom, right, top


def get_tile_top(pos):
    selected = None
    sel_top = 0
    x, y = pos

    for tile in gfw.world.objects_at(gfw.layer.tile):
        if check_valid(tile):
            l, b, r, t = tile.get_bb()
            if l <= x <= r and y > t:
                if selected is None:
                    selected = tile
                    sel_top = t
                else:
                    if t > sel_top:
                        selected = tile
                        sel_top = t
    if selected is not None:
        _, _, _, ret = selected.get_bb()
    else:
        ret = -100
    return ret


def get_tile_right(pos):
    selected = None
    sel_right = 0
    x, y = pos
    for tile in gfw.world.objects_at(gfw.layer.tile):
        if check_valid(tile):
            l, b, r, t = tile.get_bb()
            if b <= y <= t and x > r:
                if selected is None:
                    selected = tile
                    sel_right = r
                else:
                    if r > sel_right:
                        selected = tile
                        sel_right = r
    if selected is not None:
        _, _, ret, _ = selected.get_bb()
    else:
        ret = -100
    return ret


def get_tile_left(pos):
    selected = None
    sel_left = 0
    x, y = pos
    for tile in gfw.world.objects_at(gfw.layer.tile):
        if check_valid(tile):
            l, b, r, t = tile.get_bb()
            if b <= y <= t and x < l:
                if selected is None:
                    selected = tile
                    sel_left = l
                else:
                    if l < sel_left:
                        selected = tile
                        sel_left = l
    if selected is not None:
        ret, _, _, _ = selected.get_bb()
    else:
        ret = -100
    return ret


def get_tile_bottom(pos):
    selected = None
    sel_bottom = 0
    x, y = pos
    for tile in gfw.world.objects_at(gfw.layer.tile):
        if check_valid(tile):
            l, b, r, t = tile.get_bb()
            if l <= x <= r and y < b:
                if selected is None:
                    selected = tile
                    sel_bottom = b
                else:
                    if b < sel_bottom:
                        selected = tile
                        sel_bottom = b
    if selected is not None:
        _, ret, _, _ = selected.get_bb()
    else:
        ret = -100
    return ret
