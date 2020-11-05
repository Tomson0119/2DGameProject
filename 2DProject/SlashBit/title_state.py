import gfw
import gobj
from pico2d import *
from background import Background, HorzScrollBackground

BG_DIR = 'background/'

def enter():
    gfw.world.init(['bg', 'cloud', 'ui'])

    for n in range(1,4):
        bg = Background(BG_DIR + 'forest0%d.png' % n)
        gfw.world.add(gfw.layer.bg, bg)

    cloud = HorzScrollBackground(BG_DIR + 'cloud.png')
    cloud.speed = 20
    cloud.pos_y = 130
    gfw.world.add(gfw.layer.cloud, cloud)

    global title1
    title1 = gfw.font.load(gobj.res('ThaleahFat.ttf'), 140)

    global title2
    title2 = gfw.font.load(gobj.res('ThaleahFat.ttf'), 140)

    global menu1
    menu1 = gfw.font.load(gobj.res("ThaleahFat.ttf"), 50)

    global menu2
    menu2 = gfw.font.load(gobj.res("ThaleahFat.ttf"), 50)

    global exit1
    exit1 = gfw.font.load(gobj.res("ThaleahFat.ttf"), 50)

    global exit2
    exit2 = gfw.font.load(gobj.res("ThaleahFat.ttf"), 50)

def update():
    gfw.world.update()


def draw():
    gfw.world.draw()
    title1.draw(gfw.WINDOW_WIDTH // 2 - 270, gfw.WINDOW_HEIGHT // 2 - 10,
                "slash bit", color=(0, 0, 0))

    title2.draw(gfw.WINDOW_WIDTH // 2 - 280, gfw.WINDOW_HEIGHT // 2,
               "slash bit", color=(255,255,255))

    menu1.draw(gfw.WINDOW_WIDTH // 2 - 65, gfw.WINDOW_HEIGHT // 2 - 125,
                "start", color=(0, 0, 0))

    menu2.draw(gfw.WINDOW_WIDTH // 2 - 70, gfw.WINDOW_HEIGHT // 2 - 120,
               "start", color=(255, 0, 0))

    exit1.draw(gfw.WINDOW_WIDTH // 2 - 45, gfw.WINDOW_HEIGHT // 2 - 170,
               "exit", color=(0, 0, 0))

    exit2.draw(gfw.WINDOW_WIDTH // 2 - 50, gfw.WINDOW_HEIGHT // 2 - 165,
               "exit", color=(255, 255, 255))




def handle_event(e):
    event = (e.type, e.key)

    if e.type == SDL_QUIT:
        gfw.quit()
    elif event == (SDL_KEYDOWN, SDLK_ESCAPE):
        gfw.quit()
    elif event == (SDL_KEYDOWN, SDLK_DOWN):
        print("Key down pressed")


def exit():
    pass


def pause():
    pass


def resume():
    pass


if __name__ == "__main__":
    gfw.run_main()