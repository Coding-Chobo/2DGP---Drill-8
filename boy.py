from pico2d import load_image
from pico2d import get_time
#from state_machin import StateMachine
from  state_machine import *

class Boy:
    def __init__(self):
        #self.name=name
        self.x, self.y = 400, 90
        self.frame = 0
        self.dir = 0
        self.action = 3
        #self.wait_time=0;
        self.image = load_image('animation_sheet.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions({
            Run : {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle},
            Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run,time_out: Sleep,a_down: AutoRun}, 
            Sleep:{right_down: Run, left_down: Run, right_up: Run, left_up: Run, space_down: Idle},
            AutoRun: {time_out: Idle,right_down: Run, left_down: Run, right_up: Run, left_up: Run}
                        }

            )

    def update(self):
        self.state_machine.update()
        #self.frame = (self.frame + 1) % 8

    def handle_event(self, event):
        self.state_machine.add_event(('INPUT',event))
        pass

    def draw(self):
        self.state_machine.draw()
        #self.image.clip_draw(self.frame * 100, self.action * 100, 100, 100, self.x, self.y)

class Idle:
    @staticmethod
    def enter(boy,e):
        if right_down(e) or left_up(e):
            boy.action = 2
            boy.dir = -1
        elif left_down(e) or right_up(e):
            boy.action = 3
            boy.dir = 1
        elif space_down(e):
            pass
        boy.frame=0
        boy.wait_time = get_time()
        pass
        print('Boy Idle Enter')
    @staticmethod

    @staticmethod
    def exit(boy,e):
        print('Boy Idle Exit')
        pass
    @staticmethod
    def do(boy):
        boy.frame = (boy.frame+1)%8
        if get_time() - boy.wait_time>5:
            boy.state_machine.add_event(('TIME_OUT',0))
    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)

class Sleep:
    @staticmethod
    def enter(boy,e):
        if right_down(e) or left_up(e):
            boy.action = 2
            boy.dir = -1
        elif left_down(e) or right_up(e):
            boy.action, boy.frame = 3 ,0
            boy.dir = 1            
        print('Boy Sleep Enter')
        pass
    @staticmethod
    def exit(boy,e):
        pass
    @staticmethod
    def do(boy):
        boy.frame = (boy.frame+1)%8
    @staticmethod
    def draw(boy):
        if boy.dir == -1:
            boy.image.clip_composite_draw(
              boy.frame *100, boy.action*100, 100, 100,
                3.141592/2 * 3, # 90도 회전
               '', # 좌우상하 반전 X
                boy.x + 25, boy.y - 25, 100, 100
        )
        else:
              boy.image.clip_composite_draw(
              boy.frame *100, boy.action*100, 100, 100,
                3.141592/2, # 90도 회전
               '', # 좌우상하 반전 X
                boy.x - 25, boy.y - 25, 100, 100
            )

class Run:
    @staticmethod
    def enter(boy, e):
        if right_down(e) or left_up(e):
            boy.dir,boy.action=1,1
        if left_down(e) or right_up(e):
            boy.dir,boy.action= -1,0
        pass

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        if boy.dir == 1 and boy.x < 800:
            boy.x+=boy.dir*5
        elif boy.dir == -1 and boy.x > 0:
            boy.x+=boy.dir*5

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)

class Grass:
    def __init__(self):
        self.image = load_image('grass.png')
    def update(self):
        pass
    def draw(self):
        self.image.draw(400,30)

class AutoRun:
    @staticmethod
    def enter(boy, e):
        if a_down(e):
            if boy.dir == -1:
                boy.action = 0
            else :
                boy.dir,boy.action = 1,1
        boy.wait_time = get_time()
    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        if boy.x > 800:
            boy.dir = -1
            boy.frame = 0
            boy.action = 0
        if boy.x < 0:
            boy.dir = 1
            boy.frame = 0
            boy.action = 1
        if get_time() - boy.wait_time> 5 :
            boy.state_machine.add_event(('TIME_OUT',0))
            if boy.dir == 1:
                boy.action = 3
            else:
                boy.action = 2
        boy.x+=boy.dir*8

    @staticmethod
    
    def draw(boy):
            boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y,150,150)