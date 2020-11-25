import gfw
import gobj
from pico2d import *
from background import *
from player import Player


def enter():
    gfw.world.init(['bg', 'cloud', 'player', 'tile', 'enemy', 'item', 'ui'])

    for n in range(1,4):
        bg = Background('forest0%d.png' % n)
        gfw.world.add(gfw.layer.bg, bg)

    cloud = HorzScrollBackground('cloud.png', 20, 130)
    gfw.world.add(gfw.layer.cloud, cloud)

    global player
    player = Player()
    gfw.world.add(gfw.layer.player, player)


def update():
    gfw.world.update()


def draw():
    gfw.world.draw()


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