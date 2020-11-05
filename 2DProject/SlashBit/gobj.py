import gfw

RES_DIR = 'res/'

def res(name):
    return RES_DIR + name

class ImageObject:
    def __init__(self,name,pos):
        self.image = gfw.image.load(RES_DIR + name)
        self.pos = pos
    def draw(self):
        self.image.draw(*self.pos, gfw.WINDOW_WIDTH, gfw.WINDOW_HEIGHT)
    def update(self):
        pass