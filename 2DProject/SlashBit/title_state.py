import gfw
import gobj
from pico2d import *

BG_DIR = 'background/forest/'

def enter():
    gfw.world.init(['bg','cloud'])
    bg = [gobj.ImageObject(BG_DIR + 'forest01.png', (gfw.WINDOW_WIDTH // 2, gfw.WINDOW_HEIGHT // 2)),
          gobj.ImageObject(BG_DIR + 'forest02.png', (gfw.WINDOW_WIDTH // 2, gfw.WINDOW_HEIGHT // 2)),
          gobj.ImageObject(BG_DIR + 'forest03.png', (gfw.WINDOW_WIDTH // 2, gfw.WINDOW_HEIGHT // 2))]
    for obj in bg:
        gfw.world.add(gfw.layer.bg, obj)

    cloud = [gobj.ImageObject(BG_DIR + 'forest04.png',(gfw.WINDOW_WIDTH // 2, gfw.WINDOW_HEIGHT - 200)),
             gobj.ImageObject(BG_DIR + 'forest04.png', (gfw.WINDOW_WIDTH * 3 // 2, gfw.WINDOW_HEIGHT - 200))]
    for obj in cloud:
        gfw.world.add(gfw.layer.cloud, obj)


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