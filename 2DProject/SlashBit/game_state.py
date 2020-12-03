import gfw
import gobj
from pico2d import *
from background import *
from player import Player
from object import Heart
from collision_check import check_collision
import stage_gen

STAGE_GEN = True
value = 0


def enter():
    gfw.world.init(['bg', 'cloud', 'tile', 'spike', 'item', 'player', 'enemy', 'ui'])

    for n in range(1,4):
        bg = Background('forest0%d.png' % n)
        gfw.world.add(gfw.layer.bg, bg)

    cloud = HorzScrollBackground('cloud.png', 20, 130)
    gfw.world.add(gfw.layer.cloud, cloud)

    global player
    player = Player()
    gfw.world.add(gfw.layer.player, player)

    # tiles
    stage_gen.load(res('stage_01.txt'))

    # heart
    global heart
    heart = ImageObject('item/heart.png', (32, get_canvas_height() - 32), 64)

    stage_gen.update(-250 * gfw.delta_time)


def update():
    global STAGE_GEN, player, value
    gfw.world.update()
    if player.pos[0] > get_canvas_width():
        x, y = player.pos
        x = 0
        player.pos = x, y
        for tile in gfw.world.objects_at(gfw.layer.tile):
            tile.move(-get_canvas_width())
        for item in gfw.world.objects_at(gfw.layer.item):
            item.move(-get_canvas_width())
        for spike in gfw.world.objects_at(gfw.layer.spike):
            spike.move(-get_canvas_width())
        for enemy in gfw.world.objects_at(gfw.layer.enemy):
            ex, ey = enemy.pos
            ex -= get_canvas_width()
            enemy.pos = ex, ey

    check_collision(player)


def draw():
    gfw.world.draw()
    gobj.draw_collision_box()
    dx = 0
    for life in range(player.life):
        heart.draw(dx)
        dx += 32


def handle_event(e):
    event = (e.type, e.key)

    if e.type == SDL_QUIT:
        gfw.quit()
    elif event == (SDL_KEYDOWN, SDLK_ESCAPE):
        gfw.pop()

    player.handle_event(e)


def exit():
    gfw.world.clear_all()


if __name__ == "__main__":
    gfw.run_main()