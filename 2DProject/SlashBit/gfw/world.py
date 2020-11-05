import gfw
from functools import reduce

objects = []
trashbin = []

def init(layer_names):
    global objects
    objects = []
    gfw.layer = lambda: None
    layerIndex = 0
    for name in layer_names:
        objects.append([])
        gfw.layer.__dict__[name] = layerIndex
        layerIndex += 1


def add(index, obj):
    objects[index].append(obj)


def remove(obj):
    trashbin.append(obj)


def all_objects():
    for layer_objects in objects:
        for obj in layer_objects:
            yield obj


def objects_at(layer_index):
    for obj in objects[layer_index]:
        yield obj


def count_at(layer_index):
    return len(objects[layer_index])


def count():
    return reduce(lambda sum, a: sum + len(a), objects, 0)


def clear_all():
    global objects
    for obj in all_objects():
        del obj
    objects = []


def clear_at(layer_index):
    for obj in objects[layer_index]:
        del obj
    objects[layer_index] = []


def empty_trashbin():
    global trashbin

    for trash in trashbin:
        for layer_objects in objects:
            try:
                pass
                #layer_objects.remove(obj)
            except ValueError:
                pass
    trashbin = []


def draw():
    for obj in all_objects():
        obj.draw()


def update():
    for obj in all_objects():
        obj.update()
    if len(trashbin) > 0:
        empty_trashbin()

