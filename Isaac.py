from pico2d import *
import main_state
import game_framework
from Health import  Health

BackGround_Width = 1280
BackGround_Height = 960


PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 1.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH* 1000.0/ 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM/ 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS*PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 4.0 / TIME_PER_ACTION
BODYFRAME_PER_ACTION = 8
HEADFRAME_PER_ACTION = 2

class Isaac:

    def __init__(self):
        self.x, self.y = BackGround_Width//2, BackGround_Height//2
        self.frame = 0
        self.image = load_image('resorce/isaac_head.png')
        self.velocity_x = 0
        self.velocity_y = 0
        self.velocity = RUN_SPEED_PPS
        self.left = 0
        self.body_x, self.body_y = self.x-5, self.y-50
        self.body_frame = 0
        self.body_image = load_image('resorce/isaac_body.png')
        self.body_is_move = False
        self.body_bottom = 90
        self.start_health = 3
        self.now_health = 0.5
        self.health_index = self.start_health-1
        self.heartArray = [Health(60*(i+1)) for i in range(self.start_health)]
    def update(self):

        self.frame = (self.frame+ HEADFRAME_PER_ACTION*ACTION_PER_TIME*game_framework.frame_time) % 2
        if self.x > BackGround_Width-180:
            self.x = BackGround_Width-180
        elif self.x < 180:
            self.x = 180
        else:
            self.x += self.velocity_x
        if self.y > BackGround_Height-150:
            self.y = BackGround_Height-150
        elif self.y < 220:
            self.y = 220
        else:
            self.y += self.velocity_y
        if self.body_is_move:
            self.body_frame = (self.body_frame+BODYFRAME_PER_ACTION*ACTION_PER_TIME*game_framework.frame_time) % 8
        if self.body_x > BackGround_Width-185:
            self.body_x = BackGround_Width-185
        elif self.body_x < 175:
            self.body_x = 175
        else:
            self.body_x += self.velocity_x
        if self.body_y > BackGround_Height-200:
            self.body_y = BackGround_Height-200
        elif self.body_y < 170:
            self.body_y = 170
        else:
            self.body_y += self.velocity_y
        if self.now_health < self.start_health:
            if self.start_health-self.now_health <= 1:
                self.heartArray[self.health_index].heart_state = (self.start_health-self.now_health)*2
            elif self.start_health-self.now_health > 1:
                if self.start_health-self.now_health <= 2:
                    self.heartArray[self.health_index].heart_state = 2
                    self.heartArray[self.health_index-1].heart_state =(self.start_health-self.now_health) * 2 - 2
                else:
                    self.heartArray[self.health_index].heart_state = 2
                    self.heartArray[self.health_index-1].heart_state = 2
                    self.heartArray[self.health_index - 2].heart_state = (self.start_health - self.now_health) * 2 - 4

    def draw(self):
        self.body_image.clip_draw(105 * int(self.body_frame), self.body_bottom, 60, 60, self.body_x, self.body_y)
        self.image.clip_draw(int(self.frame) * 80 + self.left, 0, 80, 80, self.x, self.y)
        for Health in self.heartArray:
            Health.draw()
    pass

    def get_bb(self):
        return self.x - 20, self.y -50, self.x + 20, self.y +50




