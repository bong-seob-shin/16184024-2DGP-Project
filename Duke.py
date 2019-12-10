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

class Duke:
    image = None

    def __init__(self):
        if Duke.image == None:
            Duke.image = load_image('resource/Duke.png')
        self.x = BackGround_Width//2
        self.y = BackGround_Height//2
        self.velocity = RUN_SPEED_PPS
        self.dir = random.randint(0,1)
        self.timer = 1
        self.health = 100
        self.frame = 0
        self.bottom = 0
        self.create_fly_timer = 50
        self.build_behavior_tree()
        self.summon_sound = load_wav('sound/summon.wav')
        self.summon_sound.set_volume(50)


    def draw(self):
        self.image.clip_draw(int(self.frame) * 200, self.bottom, 200, 200, self.x, self.y)
    def get_bb(self):
        return self.x - 80, self.y - 80, self.x + 80, self.y +80

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

    def summon(self):
        self.summon_sound.play()

    pass
