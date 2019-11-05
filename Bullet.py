from pico2d import *
import game_world

class Bullet:

    image = None

    def __init__(self, x = 400, y= 300, b_dir =0):
        if Bullet.image == None:
            Bullet.image = load_image('resorce/bullet.png')
        self.x, self.y, self.b_dir = x, y, b_dir
        self.velocity = 40
        self.start_x = self.x
        self.start_y = self.y
    def draw(self):
        if self.b_dir == 0: #오른쪽
            self.image.draw(self.x+40, self.y)
        elif self.b_dir == 1: #왼쪽
            self.image.draw(self.x-40, self.y)
        elif self.b_dir == 2: #아래
            self.image.draw(self.x, self.y+40)
        elif self.b_dir == 3: #위
            self.image.draw(self.x, self.y-40)

    def update(self):
        if self.b_dir == 0: #오른쪽
            if self.x > self.start_x+300:
                self.y -= 10

                if self.velocity> 10:
                    self.velocity -= 8
            self.x += self.velocity
        elif self.b_dir == 1: #왼쪽
            if self.x < self.start_x-300:
                self.y -= 10
                if self.velocity > 10:
                    self.velocity -= 8
            self.x -= self.velocity
        elif self.b_dir == 2: #아래
            self.y += self.velocity
        elif self.b_dir == 3: #위
            self.y -= self.velocity

        if self.x < 175 or self.x > 1280 - 175:
            game_world.remove_object(self)
        elif self.x > self.start_x+400 or self.x < self.start_x-400:
            game_world.remove_object(self)

        if self.y < 155 or self.y > 960 - 150:
            game_world.remove_object(self)
        elif self.y <self.start_y - 400 or self.y > self.start_y+400:
            game_world.remove_object(self)
    pass
