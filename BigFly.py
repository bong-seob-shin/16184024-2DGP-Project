from pico2d import *
import random
from BehaviorTree import SelectorNode, SequenceNode, Node, LeafNode, BehaviorTree
import game_framework
from Isaac import  Isaac
import main_state_2

BackGround_Width = 1280
BackGround_Height = 960

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 4.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH* 1000.0/ 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM/ 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS*PIXEL_PER_METER)

TIME_PER_ACTION = 2
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION_IDLE = 2
FRAMES_PER_ACTION_SHOT = 16

class BigFly:
    image = None

    def __init__(self):
        if BigFly.image == None:
            BigFly.image = load_image('resource/BigFly.png')
        self.x = random.randint(200, 1000)
        self.y = random.randint(200, 750)
        self.velocity = RUN_SPEED_PPS
        self.dir = random.randint(0,1)
        self.timer = 5
        self.health = 5
        self.frame = 0
        self.bottom = 0
        self.build_behavior_tree()
        self.is_shot = False
        self.shot_term= 0

    def draw(self):
        draw_rectangle(*self.get_bb())
        self.image.clip_draw(int(self.frame) * 40, self.bottom, 40, 40, self.x, self.y)
    def get_bb(self):
        return self.x - 10, self.y - 10, self.x + 10, self.y +10

    def calculate_current_position(self):
        if self.is_shot:
            self.frame = (self.frame + FRAMES_PER_ACTION_IDLE * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION_SHOT
        else:
            self.frame = (self.frame + FRAMES_PER_ACTION_IDLE * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION_IDLE
        self.x += self.speed * math.cos(self.dir) * game_framework.frame_time
        self.y += self.speed * math.sin(self.dir) * game_framework.frame_time
        self.x = clamp(150, self.x, 1280 - 250)
        self.y = clamp(150, self.y, 960 - 250)

    def wander(self):
        self.is_shot = False
        self.speed = RUN_SPEED_PPS
        self.calculate_current_position()
        self.timer -= game_framework.frame_time
        if self.timer < 0:
            self.timer += 1.0
            self.dir = random.random()*2*math.pi
            if math.cos(self.dir) > 0:
                self.bottom = 40
            elif math.cos(self.dir)< 0:
                self.bottom = 0
            return BehaviorTree.SUCCESS
        pass

    def build_behavior_tree(self):
        find_player_node = LeafNode("Find Player",self.find_player)
        move_to_player_node = LeafNode("Move to Player",self.move_to_player)
        shot_to_player_node = LeafNode("Shot to Player",self.shot_to_player)
        find_node = SequenceNode("Find")
        find_node.add_children(find_player_node,move_to_player_node,shot_to_player_node)
        find_wander_node = SelectorNode("Find Wander")
        wander_node = LeafNode("Wander", self.wander)
        find_wander_node.add_children(find_node,wander_node)

        self.bt = BehaviorTree(find_wander_node)
        pass

    def update(self):
        if self.is_shot:
            self.image = load_image('resource/BigFly_Attack.png')
            self.frame = (self.frame + FRAMES_PER_ACTION_IDLE * ACTION_PER_TIME * game_framework.frame_time) % 16
            self.shot_term -= 1
        else:
            self.image = load_image('resource/BigFly.png')
            self.frame = (self.frame + FRAMES_PER_ACTION_IDLE * ACTION_PER_TIME * game_framework.frame_time) % 2
        self.bt.run()

    def find_player(self):
        isaac = main_state_2.get_isaac()
        distance = (isaac.x - self.x) ** 2 + (isaac.y - self.y) ** 2
        if distance < (PIXEL_PER_METER * 10) ** 2:
            self.dir = math.atan2(isaac.y - self.y, isaac.x - self.x)
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL
        pass

    def move_to_player(self):
        self.speed = RUN_SPEED_PPS/4
        self.calculate_current_position()
        return BehaviorTree.SUCCESS
        pass

    def shot_to_player(self):
        self.is_shot = True
        return BehaviorTree.SUCCESS
        pass

