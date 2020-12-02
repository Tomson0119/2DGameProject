import gfw
from pico2d import *


def check_blew(Player):
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
        if dx > 0:
            dx = 0
        Player.delta = dx, dy
        return True


def check_left(Player):
    left, _, _, _ = Player.get_bb()
    dx, dy = Player.delta
    if Player.tile_bound[2] < 0:
        return False
    if left <= Player.tile_bound[2]:
        if dx < 0:
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
