import gfw
import gobj
from pico2d import *
from background import *
from player import Player
from object import Heart
from collision_check import check_collision, check_valid
import stage_gen
from menu import Menu

STAGE_GEN = True
START_TIME = 0
END_TIME = 0

ImageName = None


def enter(select=None):
    gfw.world.init(['bg', 'cloud', 'tile', 'spike', 'item', 'player', 'enemy'])

    global START_TIME, END_TIME
    START_TIME = get_time()
    END_TIME = START_TIME

    for n in range(1,4):
        bg = Background('forest0%d.png' % n)
        gfw.world.add(gfw.layer.bg, bg)

    cloud = HorzScrollBackground('cloud.png', 20, 130)
    gfw.world.add(gfw.layer.cloud, cloud)

    global player, imageName
    if select == 1:
        imageName = 'soldier_animation_sheet.png'
    elif select == 2:
        imageName = 'princess_animation_sheet.png'
    player = Player(200, 200, imageName)
    gfw.world.add(gfw.layer.player, player)

    # tiles
    stage_gen.load(res('stage_01.txt'))

    # heart
    global heart
    heart = ImageObject('item/heart.png', (32, get_canvas_height() - 32), 64)

    color = [(255, 255, 255), (255, 0, 0), (0, 0, 0), (255, 255, 255)]
    init = [(140, -290, 100, "game over"), (140, -300, 110, "game over"),
            (50, -180, -75, "restart to enter"), (50, -185, -70, "restart to enter")]

    global MENU
    MENU = []
    for n, (size, pos_x, pos_y, sent) in zip(range(4), init):
        menu = Menu('ThaleahFat.ttf', size, color[n],
                    sent, pos_x, pos_y)
        MENU.append(menu)

    global TIME_STR
    TIME_STR = [Menu('ThaleahFat.ttf', 50, (0, 0, 0), "", 425, -335),
                Menu('ThaleahFat.ttf', 50, (255, 255, 255), "", 420, -330)]

    stage_gen.update(-250 * gfw.delta_time)

    global game_clear
    game_clear = False


def update():
    global STAGE_GEN, player, game_over, game_clear
    gfw.world.update()
    if player.pos[0] > get_canvas_width():
        for objects in [gfw.layer.tile, gfw.layer.item, gfw.layer.spike, gfw.layer.enemy, gfw.layer.player]:
            for obj in gfw.world.objects_at(objects):
                obj.move(-get_canvas_width())

    for enemy in gfw.world.objects_at(gfw.layer.enemy):
        if check_valid(enemy):
            enemy.activate()

    if not game_clear:
        game_clear = check_collision(player)
    game_over = player.is_dead()


def draw():
    gfw.world.draw()
    dx = 0
    for life in range(player.life):
        heart.draw(dx)
        dx += 32

    if game_over or game_clear:
        global END_TIME, TIME_STR
        if game_clear:
            player.diactivate()
            MENU[0].sentence = 'Game Clear'
            MENU[1].sentence = 'Game Clear'
        if END_TIME == START_TIME:
            END_TIME = get_time() - START_TIME
        for menu in MENU:
            menu.draw()
        for time_str in TIME_STR:
            time_str.draw(END_TIME)


def handle_event(e):
    event = (e.type, e.key)

    if e.type == SDL_QUIT:
        gfw.quit()
    elif event == (SDL_KEYDOWN, SDLK_ESCAPE):
        gfw.pop()
    elif event == (SDL_KEYDOWN, SDLK_RETURN):
        if game_over or game_clear:
            exit()
            enter()

    player.handle_event(e)


def exit():
    gfw.world.clear_all()


if __name__ == "__main__":
    gfw.run_main()