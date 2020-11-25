import gfw
from pico2d import *
from tile import Tile
import item
import gobj

UNIT_PER_LINE = 100
SCREEN_LINES = 10
BLOCK_SIZE = 96

lines = []
ASCII = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':',
         ';', '<', '=', '>', '?', '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G']


def load(file):
    global lines, current_x, create_at, map_index
    with open(file, 'r') as f:
        ch = f.readlines()
        lines = ch
    current_x = 0
    map_index = 0
    create_at = get_canvas_width() + 2 * BLOCK_SIZE


def count():
    return len(lines) // SCREEN_LINES * UNIT_PER_LINE


def update(dx):
    global current_x, create_at
    current_x += dx
    ret = True
    while current_x < create_at:
        ret = create_column()
        if not ret:
            return ret
    return ret


def create_column():
    global current_x, map_index
    y = BLOCK_SIZE // 2
    for row in range(SCREEN_LINES):
        ch = get(map_index, row)
        if ch == '#':
            return False
        create_object(ch, current_x, y)
        y += BLOCK_SIZE
    current_x += BLOCK_SIZE
    map_index += 1
    return True


def get(x, y):
    col = x % UNIT_PER_LINE
    row = x // UNIT_PER_LINE * SCREEN_LINES + SCREEN_LINES - 1 - y
    return lines[row][col]


def create_object(ch, x, y):
    if ch in ASCII:
        y -= BLOCK_SIZE // 2 + 48
        x -= BLOCK_SIZE // 2
        obj = Tile(ord(ch) - ord('0'), x, y)
        gfw.world.add(gfw.layer.tile, obj)
