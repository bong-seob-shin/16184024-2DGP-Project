from pico2d import *
import game_world
import game_framework


PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 4.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH* 1000.0/ 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM/ 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS*PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 4.0 / TIME_PER_ACTION
PER_ACTION = 8

class EnemyBulletBigFly:

    image = None

    def __init__(self, x = 400, y= 300, dir =0, speed = 1):
        if EnemyBulletBigFly.image == None:
            EnemyBulletBigFly.image = load_image('resource/enemy_nomal_bullet.png')
        self.x, self.y, self.dir = x, y, dir
        self.velocity = RUN_SPEED_PPS
        self.start_x = self.x
        self.start_y = self.y
        self.speed = RUN_SPEED_PPS*speed
        self.damage = 1
    def draw(self):


        self.image.draw(self.x, self.y)


        draw_rectangle(*self.get_bb())
    def update(self):
        self.x += self.speed * math.cos(self.dir) * game_framework.frame_time
        self.y += self.speed * math.sin(self.dir) * game_framework.frame_time

        if self.x < 175 or self.x > 1280 - 175:
            game_world.remove_object(self)
        elif self.x > self.start_x+400 or self.x < self.start_x-400:
            game_world.remove_object(self)

        if self.y < 155 or self.y > 960 - 150:
            game_world.remove_object(self)
        elif self.y <self.start_y - 400 or self.y > self.start_y+400:
            game_world.remove_object(self)

    def get_bb(self):
            return self.x - 10, self.y - 10, self.x + 10, self.y + 10




    pass

