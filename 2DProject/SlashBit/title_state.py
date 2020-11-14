import gfw
import gobj
from pico2d import *
from background import Background, HorzScrollBackground

BG_DIR = 'background/'

title = []
menu = []
index = 0


def enter():
    gfw.world.init(['bg', 'cloud', 'ui'])

    for n in range(1,4):
        bg = Background(BG_DIR + 'forest0%d.png' % n)
        gfw.world.add(gfw.layer.bg, bg)

    cloud = HorzScrollBackground(BG_DIR + 'cloud.png')
    cloud.speed = 20
    cloud.pos_y = 130
    gfw.world.add(gfw.layer.cloud, cloud)

    global title
    for n in range(2):
        title.append(gfw.font.load(gobj.res('ThaleahFat.ttf'), 140))
    for n in range(4):
        menu.append(gfw.font.load(gobj.res('ThaleahFat.ttf'), 50))


def update():
    gfw.world.update()


def draw():
    gfw.world.draw()
    title[0].draw(gfw.WINDOW_WIDTH // 2 - 270, gfw.WINDOW_HEIGHT // 2 - 10,
                "slash bit", color=(0, 0, 0))

    title[1].draw(gfw.WINDOW_WIDTH // 2 - 280, gfw.WINDOW_HEIGHT // 2,
                "slash bit", color=(255,255,255))

    menu[0].draw(gfw.WINDOW_WIDTH // 2 - 65, gfw.WINDOW_HEIGHT // 2 - 125,
                "start", color=(0, 0, 0))

    color = (255, 255, 255) if index == 1 else (255, 0, 0)
    menu[1].draw(gfw.WINDOW_WIDTH // 2 - 70, gfw.WINDOW_HEIGHT // 2 - 120,
               "start", color=color)

    menu[2].draw(gfw.WINDOW_WIDTH // 2 - 45, gfw.WINDOW_HEIGHT // 2 - 170,
               "exit", color=(0, 0, 0))

    color = (255, 255, 255) if index == 0 else (255, 0, 0)
    menu[3].draw(gfw.WINDOW_WIDTH // 2 - 50, gfw.WINDOW_HEIGHT // 2 - 165,
               "exit", color=color)




def handle_event(e):
    global index
    event = (e.type, e.key)

    if e.type == SDL_QUIT:
        gfw.quit()
    elif event == (SDL_KEYDOWN, SDLK_ESCAPE):
        gfw.quit()
    elif event == (SDL_KEYDOWN, SDLK_UP):
        index = 0
    elif event == (SDL_KEYDOWN, SDLK_DOWN):
        index = 1
    elif event == (SDL_KEYDOWN, SDLK_RETURN):
        if index == 1:
            gfw.quit()
        else:
            print("game start")



def exit():
    pass


def pause():
    pass


def resume():
    pass


if __name__ == "__main__":
    gfw.run_main()