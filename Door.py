from pico2d import *
import main_state

class Door:
    def __init__(self):
        self.image = load_image('resorce/door.png')
        self.x = 0
        self.y = main_state.BackGround_Height//2
    def update(self):
        pass

    def draw(self):
        if self.x < main_state.BackGround_Width//2:
            self.image.composite_draw(0,'h',self.x,self.y)
        else:
            self.image.draw(self.x, self.y)



class InDoor():
    def __init__(self):
        self.image = load_image('resorce/close_door.png')
        self.x = 0
        self.y = main_state.BackGround_Height//2
        self.open_door = False
    def update(self):
        if self.open_door:
            self.image = load_image('resorce/open_door.png')
        pass

    def draw(self):
        if self.x < main_state.BackGround_Width // 2:
            self.image.composite_draw(0, 'h', self.x, self.y)
        else:
            self.image.draw(self.x, self.y)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 20, self.y - 40, self.x + 20, self.y + 40


