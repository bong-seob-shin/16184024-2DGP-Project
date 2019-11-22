from pico2d import *
import game_world

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 4.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH* 1000.0/ 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM/ 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS*PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 4.0 / TIME_PER_ACTION
PER_ACTION = 8

class Bullet:

    image = None

    def __init__(self, x = 400, y= 300, b_dir =0):
        if Bullet.image == None:
            Bullet.image = load_image('resorce/bullet.png')
        self.x, self.y, self.b_dir = x, y, b_dir
        self.right_x, self.left_x, self.up_y, self.down_y = x+40, x-40, y+40, y-40
        self.velocity = RUN_SPEED_PPS
        self.start_x = self.x
        self.start_y = self.y
        self.damage = 1
    def draw(self):

        if self.b_dir == 0: #오른쪽
            self.image.draw(self.right_x, self.y)
        elif self.b_dir == 1: #왼쪽
            self.image.draw(self.left_x, self.y)
        elif self.b_dir == 2: #아래
            self.image.draw(self.x, self.up_y)
        elif self.b_dir == 3: #위
            self.image.draw(self.x, self.down_y)
        draw_rectangle(*self.get_bb())
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

        self.right_x = self.x + 40
        self.left_x = self.x - 40
        self.up_y = self.y + 40
        self.down_y = self.y - 40
    def get_bb(self):
        if self.b_dir == 0:  # 오른쪽
            return self.right_x - 20, self.y - 20, self.right_x + 20, self.y + 20
        elif self.b_dir == 1:  # 왼쪽
            return self.left_x - 20, self.y - 20, self.left_x + 20, self.y + 20
        elif self.b_dir == 2:  # 아래
            return self.x - 20, self.up_y - 20, self.x + 20, self.up_y + 20
        elif self.b_dir == 3:  # 위
            return self.x - 20, self.down_y - 20, self.x + 20, self.down_y + 20



    pass

