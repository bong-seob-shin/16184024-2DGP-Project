from pico2d import *
import main_state


class Rock:
    def __init__(self,x , y):
        self.image = load_image('resource/rock.png')
        self.x = x
        self.y = y

    def update(self):
     pass

    def draw(self):
        self.image.draw(self.x, self.y)
        draw_rectangle(*self.get_bb())


    def get_bb(self):
        return self.x - 30, self.y - 30, self.x + 30, self.y + 30


