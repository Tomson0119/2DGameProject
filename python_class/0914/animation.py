from pico2d import *

open_canvas()

gr = load_image('res/grass.png')
ch = load_image('res/animation_sheet.png')

x = 0
frame_index = 0
action = 0

while x < 810:
    clear_canvas()
    gr.draw(400,30)
    ch.clip_draw(frame_index * 100, action * 100, 100, 100, x, 85)
    update_canvas()

    # get_events()

    x += 2

    if x % 100 == 0:
        action = (action + 1) % 4

    frame_index = (frame_index + 1) % 8

    delay(0.03)

delay(2)
close_canvas()
