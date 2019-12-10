from pico2d import *
import random
from BehaviorTree import SelectorNode, SequenceNode, Node, LeafNode, BehaviorTree
import game_framework
from Isaac import  Isaac


BackGround_Width = 1280
BackGround_Height = 960

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 4.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH* 1000.0/ 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM/ 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS*PIXEL_PER_METER)

TIME_PER_ACTION = 2
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4

class Fly:
    image = None

    def __init__(self):
        if Fly.image == None:
            Fly.image = load_image('resource/Fly.png')
        self.x = random.randint(200, 1000)
        self.y = random.randint(200, 750)
        self.velocity = RUN_SPEED_PPS
        self.dir = random.randint(0,1)
        self.timer = 1
        self.health = 2
        self.frame = 0
        self.bottom = 0
        self.build_behavior_tree()


    def draw(self):
        draw_rectangle(*self.get_bb())
        self.image.clip_draw(int(self.frame) * 20, self.bottom, 20, 20, self.x, self.y)
    def get_bb(self):
        return self.x - 10, self.y - 10, self.x + 10, self.y +10

    def calculate_current_position(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        self.x += self.speed * math.cos(self.dir) * game_framework.frame_time
        self.y += self.speed * math.sin(self.dir) * game_framework.frame_time
        self.x = clamp(150, self.x, 1280 - 250)
        self.y = clamp(150, self.y, 960 - 250)

    def wander(self):
        self.speed = RUN_SPEED_PPS
        self.calculate_current_position()
        self.timer -= game_framework.frame_time
        if self.timer < 0:
            self.timer += 1.0
            self.dir = random.random()*2*math.pi
            if math.cos(self.dir) > 0:
                self.bottom = 20
            elif math.cos(self.dir)< 0:
                self.bottom = 0
            return BehaviorTree.SUCCESS
        pass

    def build_behavior_tree(self):
        wander_node = LeafNode("Wander", self.wander)
        self.bt = BehaviorTree(wander_node)
        pass

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        self.bt.run()


    pass
