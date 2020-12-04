import gfw
import gobj
from pico2d import *
from background import *
from player import Player
from menu import Menu
from character import Character
import game_state

menu_music = None


def enter():
    gfw.world.init(['bg', 'cloud', 'character', 'ui'])

    for n in range(1,4):
        bg = Background('forest0%d.png' % n)
        gfw.world.add(gfw.layer.bg, bg)

    cloud = HorzScrollBackground('cloud.png', 20, 130)
    gfw.world.add(gfw.layer.cloud, cloud)

    global soldier, princess
    soldier = Character(400, 300, 'soldier_animation_sheet-tile.png')
    soldier.set_animation(True)
    gfw.world.add(gfw.layer.character, soldier)

    princess = Character(get_canvas_width() - 400, 300, 'princess_animation_sheet-tile.png')
    gfw.world.add(gfw.layer.character, princess)

    color = [(0, 0, 0), (255, 255, 255)]
    init = [(100, -365, 200, "select character"), (100, -370, 210, "select character"),
            (50, -305, -305, "soldier"), (50, -310, -300, "soldier"),
            (50, 150, -305, "princess"), (50, 145, -300, "princess")]

    for n, (size, pos_x, pos_y, sent) in zip(range(6), init):
        menu = Menu('ThaleahFat.ttf', size, color[n % 2],
                    sent, pos_x, pos_y)
        gfw.world.add(gfw.layer.ui, menu)

    global ret
    ret = 1

    global menu_music
    menu_music = load_wav(res('sound/menu.wav'))
    menu_music.set_volume(10)


def update():
    gfw.world.update()


def draw():
    gfw.world.draw()


def handle_event(e):
    global soldier, princess, ret, menu_music
    event = (e.type, e.key)

    if e.type == SDL_QUIT:
        gfw.quit()
    elif event == (SDL_KEYDOWN, SDLK_ESCAPE):
        gfw.pop()
    elif event == (SDL_KEYDOWN, SDLK_LEFT):
        menu_music.play()
        ret = 1
        soldier.set_animation(True)
        princess.set_animation(False)
    elif event == (SDL_KEYDOWN, SDLK_RIGHT):
        menu_music.play()
        ret = 2
        soldier. set_animation(False)
        princess.set_animation(True)
    elif event == (SDL_KEYDOWN, SDLK_RETURN):
        gfw.push(game_state, ret)


def exit():
    global menu_music
    gfw.world.clear_all()
    if menu_music is not None:
        del menu_music


if __name__ == "__main__":
    gfw.run_main()