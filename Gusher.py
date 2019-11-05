from pico2d import *
import random

BackGround_Width = 1280
BackGround_Height = 960


class Gusher:
    image = None

    def __init__(self):
        if Gusher.image == None:
            Gusher.image = load_image('resorce/Gusher.png')
        self.x = BackGround_Width//2 + 100
        self.y = BackGround_Height//2
        self.velocity = 20
        self.dir = 1
        self.timer = 5

    def update(self):
        self.timer -= 1
        if self.timer == 0:
            self.dir = random.randint(1, 4)
            self.timer = 5
        if self.dir == 1 :
           self.x = self.x + self.velocity
        elif self.dir == 2:
            self.x = self.x - self.velocity
        elif self.dir == 3:
            self.y = self.y + self.velocity
        elif self.dir == 4:
            self.y = self.y - self.velocity

        if self.x > BackGround_Width-180:
            self.x = BackGround_Width-180
        elif self.x < 180:
            self.x = 180
        if self.y > BackGround_Height-150:
            self.y = BackGround_Height-150
        elif self.y < 220:
            self.y = 220

    def draw(self):
        self.image.draw(self.x, self.y, 100, 100)

    pass
