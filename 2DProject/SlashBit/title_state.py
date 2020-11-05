import gfw
import gobj
from pico2d import *
from background import Background

BG_DIR = 'background/'

def enter():
    gfw.world.init(['bg', 'cloud'])

    for n in range(1,4):
        bg = Background(BG_DIR + 'forest0%d.png' % n)
        gfw.world.add(gfw.layer.bg, bg)


def update():
    gfw.world.update()


def draw():
    gfw.world.draw()


def handle_event(e):
    if e.type == SDL_QUIT:
        gfw.quit()
    elif (e.type, e.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
        gfw.quit()


def exit():
    pass


def pause():
    pass


def resume():
    pass


if __name__ == "__main__":
    gfw.run_main()