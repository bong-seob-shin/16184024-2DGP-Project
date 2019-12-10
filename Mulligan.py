from pico2d import *
import random
from BehaviorTree import SelectorNode, SequenceNode, Node, LeafNode, BehaviorTree
import game_framework
from Isaac import  Isaac
import main_state_3

BackGround_Width = 1280
BackGround_Height = 960

PIXEL_PER_METER = (10.0 / 0.1)
RUN_SPEED_KMPH = 3.5
RUN_SPEED_MPM = (RUN_SPEED_KMPH* 1000.0/ 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM/ 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS*PIXEL_PER_METER)

TIME_PER_ACTION = 2
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 6

class Mulligan:
    image = None

    def __init__(self):
        if Mulligan.image == None:
            Mulligan.image = load_image('resource/mulligan.png')
        self.x = random.randint(200, 1000)
        self.y = random.randint(200, 750)
        self.speed = RUN_SPEED_PPS
        self.dir = random.randint(0,1)
        self.timer = 1
        self.health = 7
        self.frame = 0
        self.bottom = 0
        self.build_behavior_tree()


    def draw(self):
        self.image.clip_draw(int(self.frame) * 100, self.bottom, 80, 40, self.x, self.y)
    def get_bb(self):
        return self.x - 40, self.y - 20, self.x + 40, self.y +20

    def calculate_current_position(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        self.x += self.speed * math.cos(self.dir) * game_framework.frame_time
        self.y += self.speed * math.sin(self.dir) * game_framework.frame_time
        self.x = clamp(150, self.x, 1280 - 250)
        self.y = clamp(150, self.y, 960 - 250)


    def find_player_for_runaway(self):
        isaac = main_state_3.get_isaac()
        distance = (isaac.x - self.x) ** 2 + (isaac.y - self.y) ** 2
        if distance < (PIXEL_PER_METER * 10) ** 2:
            self.dir = -math.atan2(isaac.y-self.y, self.x- isaac.x)
            if self.dir > 0:
                self.bottom = 0
            elif self.dir <= 0:
                self.bottom = 40
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL
        pass

    def move_to_player(self):
        self.speed = RUN_SPEED_PPS
        self.calculate_current_position()
        self.dir = self.dir*-1
        return BehaviorTree.SUCCESS
        pass


    def build_behavior_tree(self):
        find_player_for_runaway_node = LeafNode("Find Player for Runaway", self.find_player_for_runaway)
        move_to_player_node = LeafNode("Move to Player", self.move_to_player)
        runaway_node = SequenceNode("Runaway")
        runaway_node.add_children(find_player_for_runaway_node,move_to_player_node)
        self.bt = BehaviorTree(runaway_node)
        pass

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6
        self.bt.run()


    pass
