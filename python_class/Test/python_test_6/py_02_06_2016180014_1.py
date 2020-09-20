import helper
from pico2d import *

# Class
class Grass:
    def __init__(self, pos):
        self.pos = pos
        self.image = load_image('../res/grass.png')
    def draw(self):
        self.image.draw(self.pos[0], self.pos[1])

class Boy:
    def __init__(self, pos):
        self.pos = pos
        self.delta = (0,0)
        self.finx = 0
        self.image = load_image('../res/run_animation.png')

    def draw(self):
        self.image.clip_draw(self.finx * 100, 0, 100, 100, self.pos[0], self.pos[1])

# ---------------------------------------


# Function
def draw():
    clear_canvas()
    gras.draw()
    boy.draw()
    update_canvas()

def handle_events():
    global loop, speed

    events = get_events()
    for e in events:
        if e.type == SDL_QUIT:
            loop = False
        elif e.type == SDL_KEYDOWN:
            if e.key == SDLK_ESCAPE:
                loop = False
        elif e.type == SDL_MOUSEBUTTONDOWN:
            temp_target = (e.x, get_canvas_height() - e.y)
            size = len(targets)
            speed += 1

            if size == 0 or (size > 0 and temp_target != targets[size - 1]):
                targets.append(temp_target)

            print("Clicked! (X : {} Y : {})".format(temp_target[0], temp_target[1]))
            print(targets)

def update():
    global done, target, speed

    if boy.pos != target:
        boy.finx = (boy.finx + 1) % 8
    else:
        if targets:
            target = targets.pop(0)
        else:
            speed = 0
        boy.finx = 0

    delta = helper.delta(boy.pos, target, speed)
    boy.pos, done = helper.move_toward(boy.pos, delta, target)

# ---------------------------------------


# Main
if __name__=="__main__":
    open_canvas()

    gras = Grass(pos=(401, 31))
    boy = Boy(pos=(400, 82))

    loop = True
    done = False
    speed = 0

    target = boy.pos
    targets = []

    while loop:
        draw()
        handle_events()
        update()
        delay(0.05)

    close_canvas()