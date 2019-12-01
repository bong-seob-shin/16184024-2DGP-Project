from pico2d import *
import random
from BehaviorTree import SelectorNode, SequenceNode, Node, LeafNode, BehaviorTree
import game_framework
from Isaac import  Isaac
import main_state_4

BackGround_Width = 1280
BackGround_Height = 960

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 2.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH* 1000.0/ 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM/ 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS*PIXEL_PER_METER)

TIME_PER_ACTION = 2
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION_IDLE = 4
FRAMES_PER_ACTION_RUSH = 1

class Maggot:
    image = None

    def __init__(self):
        if Maggot.image == None:
            Maggot.image = load_image('resource/maggot.png')
        self.x = random.randint(200, 1000)
        self.y = random.randint(200, 750)
        self.velocity = RUN_SPEED_PPS
        self.dir = random.randint(0,3)
        self.timer = 5
        self.health = 5
        self.frame = 0
        self.bottom = 0
        self.build_behavior_tree()
        self.is_rush = False
        self.shot_term= 0

    def draw(self):
        draw_rectangle(*self.get_bb())
        self.image.clip_draw(int(self.frame) * 60, self.bottom, 60, 60, self.x, self.y)
    def get_bb(self):
        return self.x - 10, self.y - 10, self.x + 10, self.y +10

    def calculate_current_position(self):

        if self.dir == 0:
            self.y += self.speed * game_framework.frame_time
            if self.y == clamp(150, self.y, 960 - 250):
                self.is_rush = False
        elif self.dir == 1:
            self.y -= self.speed * game_framework.frame_time
            if self.y == clamp(150, self.y, 960 - 250):
                self.is_rush =False
        elif self.dir == 2 :
            self.x += self.speed * game_framework.frame_time
            if self.x == clamp(150, self.x, 1280 - 250):
                self.is_rush = False
        elif self.dir == 3 :
            self.x -= self.speed * game_framework.frame_time
            if self.x == clamp(150, self.x, 1280 - 250):
                self.is_rush = False

    def wander(self):
        self.is_rush = False
        self.speed = RUN_SPEED_PPS
        self.calculate_current_position()
        self.timer -= game_framework.frame_time
        if self.timer < 0:
            self.timer += 1.0
            self.dir = random.randint(0,3)
            if self.dir == 0:#하
                self.bottom = 0
            elif self.dir == 1:#상
                self.bottom = 60
            elif self.dir == 2:#좌
                self.bottom = 120
            elif self.dir == 3:#우
                self.bottom = 180
            return BehaviorTree.SUCCESS
        pass

    def build_behavior_tree(self):
        find_player_node = LeafNode("Find Player",self.find_player)
        move_to_player_node = LeafNode("Move to Player",self.move_to_player)
        find_node = SequenceNode("Find")
        find_node.add_children(find_player_node,move_to_player_node)
        find_wander_node = SelectorNode("Find Wander")
        wander_node = LeafNode("Wander", self.wander)
        find_wander_node.add_children(find_node,wander_node)

        self.bt = BehaviorTree(find_wander_node)
        pass

    def update(self):
        if self.is_rush:
            self.frame = 4
        else:
            self.frame = (self.frame + FRAMES_PER_ACTION_IDLE * ACTION_PER_TIME * game_framework.frame_time) % 4
        self.bt.run()

    def find_player(self):
        isaac = main_state_4.get_isaac()
        if isaac.x == self.x:
            if isaac.y <= self.y:
                self.dir = 0
                self.is_rush = True
                return BehaviorTree.SUCCESS
            elif isaac.y > self.y:
                self.dir = 1
                self.is_rush = True
                return BehaviorTree.SUCCESS
        elif isaac.y == self.y:
            if isaac.x <= self.x:
                self.dir =2
                self.is_rush = True
                return BehaviorTree.SUCCESS
            elif isaac.x > self.y:
                self.dir =3
                self.is_rush = True
                return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL
        pass

    def move_to_player(self):
        while(self.is_rush):
            self.speed = RUN_SPEED_PPS
            self.calculate_current_position()
        return BehaviorTree.SUCCESS
        pass



