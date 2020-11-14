import gfw
import gobj
from pico2d import *
from background import Background, HorzScrollBackground
from menu import Menu

index = 0


def enter():
    gfw.world.init(['bg', 'cloud', 'ui'])

    for n in range(1,4):
        bg = Background('forest0%d.png' % n)
        gfw.world.add(gfw.layer.bg, bg)

    cloud = HorzScrollBackground('cloud.png', 20, 130)
    gfw.world.add(gfw.layer.cloud, cloud)

    color = [(0, 0, 0), (255, 255, 255)]
    init = [ (140, -270, -10, "slash bit"), (140, -280, 0, "slash bit"),
             (50, -65, -125, "start"), (50, -70, -120, "start"),
             (50, -45, -170, "exit"), (50, -50, -165, "exit") ]

    global select1, select2
    for n, (size, pos_x, pos_y, sent) in zip(range(6), init):
        menu = Menu('ThaleahFat.ttf', size, color[n % 2],
                    sent, pos_x, pos_y)
        gfw.world.add(gfw.layer.ui, menu)
        if n == 3:
            select1 = menu
        if n == 5:
            select2 = menu
    select1.color = (255, 0, 0)

def update():
    gfw.world.update()


def draw():
    gfw.world.draw()


def handle_event(e):
    global index
    event = (e.type, e.key)

    if e.type == SDL_QUIT:
        gfw.quit()
    elif event == (SDL_KEYDOWN, SDLK_ESCAPE):
        gfw.quit()
    elif event == (SDL_KEYDOWN, SDLK_UP):
        index = 0
        select1.color = (255, 0, 0)
        select2.color = (255, 255, 255)
    elif event == (SDL_KEYDOWN, SDLK_DOWN):
        index = 1
        select1.color = (255, 255, 255)
        select2.color = (255, 0, 0)
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