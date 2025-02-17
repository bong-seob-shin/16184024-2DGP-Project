from pico2d import *
import game_world

PIXEL_PER_METER = (10.0 / 0.4)
RUN_SPEED_KMPH = 0.5
RUN_SPEED_MPM = (RUN_SPEED_KMPH* 1000.0/ 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM/ 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS*PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 4.0 / TIME_PER_ACTION
PER_ACTION = 8

class BlackBullet:

    image = None

    def __init__(self, x = 400, y= 300, b_dir =0):
        if BlackBullet.image == None:
            BlackBullet.image = load_image('resource/Black_Bullet.png')
        self.x, self.y, self.b_dir = x, y, b_dir
        self.right_x, self.left_x, self.up_y, self.down_y = x+40, x-40, y+40, y-40
        self.velocity = RUN_SPEED_PPS
        self.start_x = self.x
        self.start_y = self.y
        self.damage = 3
        self.sound = load_wav('sound/tearPop.wav')
        self.sound.set_volume(50)
        self.sound.play()
        self.pop_sound = load_wav('sound/pop.wav')
        self.pop_sound.set_volume(30)
    def draw(self):

        if self.b_dir == 0: #오른쪽
            self.image.draw(self.right_x, self.y)
        elif self.b_dir == 1: #왼쪽
            self.image.draw(self.left_x, self.y)
        elif self.b_dir == 2: #아래
            self.image.draw(self.x, self.up_y)
        elif self.b_dir == 3: #위
            self.image.draw(self.x, self.down_y)
    def update(self):

        if self.b_dir == 0: #오른쪽
            if self.x > self.start_x+380:
                self.y -= 1
                if self.velocity> 10:
                    self.velocity -= 55
            self.x += self.velocity

        elif self.b_dir == 1: #왼쪽
            if self.x < self.start_x-380:
                self.y -= 1
                if self.velocity > 10:
                    self.velocity -= 55
            self.x -= self.velocity

        elif self.b_dir == 2: #아래
            self.y += self.velocity

        elif self.b_dir == 3: #위
            self.y -= self.velocity

        if self.x < 175 or self.x > 1280 - 175:
            game_world.remove_object(self)
            self.pop_sound.play()

        elif self.x > self.start_x+400 or self.x < self.start_x-400:
            game_world.remove_object(self)
            self.pop_sound.play()

        if self.y < 155 or self.y > 960 - 150:
            game_world.remove_object(self)
            self.pop_sound.play()

        elif self.y <self.start_y - 400 or self.y > self.start_y+400:
            game_world.remove_object(self)
            self.pop_sound.play()

        self.right_x = self.x + 40
        self.left_x = self.x - 40
        self.up_y = self.y + 40
        self.down_y = self.y - 40
    def get_bb(self):
        if self.b_dir == 0:  # 오른쪽
            return self.right_x - 15, self.y - 15, self.right_x + 15, self.y + 15
        elif self.b_dir == 1:  # 왼쪽
            return self.left_x - 15, self.y - 15, self.left_x + 15, self.y + 15
        elif self.b_dir == 2:  # 아래
            return self.x - 15, self.up_y - 15, self.x + 15, self.up_y + 15
        elif self.b_dir == 3:  # 위
            return self.x - 15, self.down_y - 15, self.x + 15, self.down_y + 15




    pass

