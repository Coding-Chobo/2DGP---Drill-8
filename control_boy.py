from pico2d import *
import random
from boy import *

# 클래스 단위로 분리
# Game object class here
5


#event_boy=0
def handle_events():
    global running
    #global event_boy
    events = get_events()
    for event in events:
        #if event.type==SDL_KEYDOWN:
            #if event.key ==SDLK_RIGHT:
                #event_boy=1

        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            if event.type == SDL_KEYDOWN or event.type == SDL_KEYUP:
                boy.handle_event(event)
            


def reset_world():
    global running
    global grass
    global team
    global world
    global boy

    running = True
    world = []

    grass = Grass()
    world.append(grass)

    boy = Boy()
    world.append(boy)



def update_world():
    for o in world:
        o.update()
    pass


def render_world():
    clear_canvas()
    for o in world:
        o.draw()
    update_canvas()


open_canvas()
reset_world()
# game loop
while running:
    handle_events()
    update_world()
    render_world()
    delay(0.01)
# finalization code
close_canvas()
