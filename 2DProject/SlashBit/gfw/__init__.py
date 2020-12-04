from pico2d import *
import time
import gfw.world
import gfw.image
import gfw.font

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

running = True
stack = None
interval = 0.0006
delta_time = 0


def quit():
    global running
    running = False


def run(start_state):
    global running, stack
    running = True
    stack = [start_state]

    open_canvas(WINDOW_WIDTH, WINDOW_HEIGHT, False, True)

    start_state.enter()

    global delta_time
    last_time = time.time()
    while running:
        # Get deleta_time
        now = time.time()
        delta_time = now - last_time
        last_time = now

        # Event handling
        events = get_events()
        for e in events:
            stack[-1].handle_event(e)

        # Game logic
        stack[-1].update()

        # Draw
        clear_canvas()
        stack[-1].draw()
        update_canvas()

        delay(interval)

    while len(stack) > 0:
        stack[-1].exit()
        stack.pop()

    close_canvas()


def change(state):
    global stack
    if len(stack) > 0:
        stack.pop().exit()
    stack.append(state)
    state.enter()


def push(state, select=None):
    global stack
    if len(stack) > 0:
        stack[-1].exit()
    stack.append(state)
    if select is not None:
        state.enter(select)
    else:
        state.enter()


def pop():
    global stack
    size = len(stack)
    if size == 1:
        quit()
    elif size > 1:
        stack[-1].exit()
        stack.pop()
        stack[-1].enter()


def run_main():
    import sys
    main_module = sys.modules['__main__']
    run(main_module)