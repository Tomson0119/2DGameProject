from pico2d import *

# Rendering Function
def draw():
    global frame_index, action, x, y

    clear_canvas()
    gr.draw(400, 30)
    ch.clip_draw(frame_index * 100, action * 100, 100, 100, x, y)
    update_canvas()


# Handle Events
def handle_events():
    global loop, action, dx, x, y, frame_index

    events = get_events()
    for e in events:
        if e.type == SDL_QUIT:
            loop = False
        elif e.type == SDL_KEYDOWN:
            if e.key == SDLK_ESCAPE:
                loop = False
            elif e.key == SDLK_LEFT:
                action = 0
                dx -= 1
                frame_index = 0
            elif e.key == SDLK_RIGHT:
                action = 1
                dx += 1
                frame_index = 0
        elif e.type == SDL_KEYUP:
            if e.key == SDLK_LEFT:
                dx += 1
            elif e.key == SDLK_RIGHT:
                dx -= 1
        elif e.type == SDL_MOUSEMOTION:
            x, y = e.x, get_canvas_height() - e.y - 1


# Update logic
def update():
    global x, frame_index, dx

    x += dx
    if dx < 0:
        frame_index -= dx
    else:
        frame_index += dx

    if frame_index >= 7 or frame_index < 0:
        frame_index = 0


# Main Function
open_canvas()
hide_cursor()

gr = load_image('res/grass.png')
ch = load_image('res/animation_sheet.png')

x, y = get_canvas_width() // 2, 85

loop = True
dx = 0
frame_index = 0
action = 0

while loop:
    draw()
    handle_events()
    update()
    delay(0.01)

close_canvas()
# End of the code

# 프로그램 쪼개기 = 모듈화 (함수, 라이브러리, 파일)
