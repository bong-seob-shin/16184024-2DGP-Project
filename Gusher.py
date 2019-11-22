from pico2d import *
import random
from BehaviorTree import SelectorNode, SequenceNode, Node, LeafNode, BehaviorTree
import game_framework
from Isaac import  Isaac


BackGround_Width = 1280
BackGround_Height = 960

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 2.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH* 1000.0/ 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM/ 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS*PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 4.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 1

class Gusher:
    image = None

    def __init__(self):
        if Gusher.image == None:
            Gusher.image = load_image('resorce/Gusher.png')
        self.x = BackGround_Width//2 + 100
        self.y = BackGround_Height//2
        self.velocity = RUN_SPEED_PPS
        self.dir = 1
        self.timer = 5
        self.health = 10
        self.build_behavior_tree()
        self.frame = 1
    def update(self):
        self.bt.run()
        # self.timer -= 1
        # if self.timer == 0:
        #     self.dir = random.randint(1, 4)
        #     self.timer = 5
        # if self.dir == 1 :
        #    self.x = self.x + self.velocity
        # elif self.dir == 2:
        #     self.x = self.x - self.velocity
        # elif self.dir == 3:
        #     self.y = self.y + self.velocity
        # elif self.dir == 4:
        #     self.y = self.y - self.velocity
        #
        # if self.x > BackGround_Width-180:
        #     self.x = BackGround_Width-180
        # elif self.x < 180:
        #     self.x = 180
        # if self.y > BackGround_Height-150:
        #     self.y = BackGround_Height-150
        # elif self.y < 220:
        #     self.y = 220

    def draw(self):
        self.image.draw(self.x, self.y, 100, 100)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 30, self.y -30, self.x + 30, self.y +20

    def calculate_current_position(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        self.x += self.speed * math.cos(self.dir) * game_framework.frame_time
        self.y += self.speed * math.sin(self.dir) * game_framework.frame_time
        self.x = clamp(50, self.x, 1280 - 50)
        self.y = clamp(50, self.y, 1024 - 50)

    def wander(self):
        self.speed = RUN_SPEED_PPS
        self.calculate_current_position()
        self.timer -= game_framework.frame_time
        if self.timer < 0:
            self.timer += 1.0
            self.dir = random.random()*2*math.pi

            return BehaviorTree.SUCCESS
        pass

    def build_behavior_tree(self):
        wander_node = LeafNode("Wander", self.wander())
        self.bt = BehaviorTree(wander_node)
        pass


    pass
