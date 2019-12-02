from pico2d import *
import main_state


class Needle:
    def __init__(self,x , y):
        self.image = load_image('resource/needle_down.png')
        self.x = x
        self.y = y
        self.needle_up = True
        self.damage= 1
        self.timer = 10
    def update(self):
        if self.needle_up:
            self.image = load_image('resource/needle_up.png')
        else:
            self.image = load_image('resource/needle_down.png')
        pass
        self.timer -= 1
        if self.timer == 0:
            self.timer = 10
    def draw(self):
        self.image.draw(self.x, self.y)
        draw_rectangle(*self.get_bb())

    def change_needle_state(self):

        if self.needle_up:
            self.needle_up = False
        else:
            self.needle_up =True

    def get_bb(self):
        return self.x - 30, self.y - 30, self.x + 30, self.y + 30


