import random
import json
import os

from pico2d import *
import game_world
import game_framework
import pause_state
from Gusher import Gusher
from Bullet import Bullet
from BackGround import BackGround
from Isaac import Isaac

BackGround_Width = 1280
BackGround_Height = 960

name = "MainState"

character_head = None
character_body = None
background = None
font = None
bullet = None

class IssacHead:

    def __init__(self):
        self.x, self.y = BackGround_Width//2, BackGround_Height//2
        self.frame = 0
        self.image = load_image('resorce/isaac_head.png')
        self.velocity_x = 0
        self.velocity_y = 0
        self.left = 0
    def update(self):
        self.frame = (self.frame+1) % 2
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
    def draw(self):
        self.image.clip_draw(self.frame*80+self.left, 0, 80, 80, self.x, self.y)
    pass


class IssacBody:

    def __init__(self):
        self.x, self.y = BackGround_Width//2-5, (BackGround_Height//2)-50
        self.frame = 0
        self.image = load_image('resorce/isaac_body.png')
        self.velocity_x = 0
        self.velocity_y = 0
        self.is_move = False
        self.bottom = 90
    def update(self):
        if self.is_move:
            self.frame = (self.frame+1) % 8
        if self.x > BackGround_Width-185:
            self.x = BackGround_Width-185
        elif self.x < 175:
            self.x = 175
        else:
            self.x += self.velocity_x
        if self.y > BackGround_Height-200:
            self.y = BackGround_Height-200
        elif self.y < 170:
            self.y = 170
        else:
            self.y += self.velocity_y

    def draw(self):
        self.image.clip_draw(105*self.frame, self.bottom, 60, 60, self.x, self.y)




def enter():
    global isaac, background, is_key_pressed , is_key_pressing, bullet_dir, gusher
    global BackGround_Width, BackGround_Height
    BackGround_Width = 1280
    BackGround_Height = 960
    isaac = Isaac()
    gusher = Gusher()
    background = BackGround()
    game_world.add_object(background, 0)
    game_world.add_object(isaac, 1)
    game_world.add_object(gusher, 1)
    is_key_pressed = 0
    is_key_pressing = 0
    bullet_dir = 0
    pass

def exit():
    game_world.clear()
    pass


def pause():
    pass


def resume():
    pass


def handle_events():
    global is_key_pressed
    global is_key_pressing
    global bullet_dir
    global isaac

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_p:
            game_framework.push_state(pause_state)
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False
            elif event.key == SDLK_d:
                isaac.body_is_move = True
                isaac.velocity_x += 20
                isaac.body_bottom = 0
                is_key_pressed += 1
            elif event.key == SDLK_a:
                isaac.body_is_move = True
                isaac.velocity_x -= 20
                isaac.body_bottom = 180
                is_key_pressed += 1
            elif event.key == SDLK_w:
                isaac.body_is_move = True
                isaac.velocity_y += 20
                isaac.body_bottom = 90
                is_key_pressed += 1
            elif event.key == SDLK_s:
                isaac.body_is_move = True
                isaac.velocity_y -= 20
                isaac.body_bottom = 90
                is_key_pressed += 1
            elif event.key == SDLK_RIGHT:
                isaac.left = 160
                is_key_pressing += 1
                bullet_dir = 0
            elif event.key == SDLK_LEFT:
                isaac.left = 480
                is_key_pressing += 1
                bullet_dir = 1
            elif event.key == SDLK_UP:
                isaac.left = 320
                is_key_pressing += 1
                bullet_dir = 2
            elif event.key == SDLK_DOWN:
                isaac.left = 0
                is_key_pressing += 1
                bullet_dir = 3
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_d:
                is_key_pressed -= 1
                if is_key_pressed == 0:
                    isaac.body_is_move = False
                    isaac.body_frame = 0
                isaac.velocity_x -= 20
            elif event.key == SDLK_a:
                is_key_pressed -= 1
                if is_key_pressed == 0:
                    isaac.body_is_move = False
                    isaac.body_frame = 0
                isaac.velocity_x += 20
            elif event.key == SDLK_w:
                is_key_pressed -= 1
                if is_key_pressed == 0:
                    isaac.body_is_move = False
                    isaac.body_frame = 0
                isaac.velocity_y -= 20
            elif event.key == SDLK_s:
                is_key_pressed -= 1
                if is_key_pressed == 0:
                    isaac.body_is_move = False
                    isaac.body_frame = 0
                isaac.velocity_y += 20
            elif event.key == SDLK_RIGHT:
                is_key_pressing -= 1
            elif event.key == SDLK_LEFT:
                is_key_pressing -= 1
            elif event.key == SDLK_UP:
                is_key_pressing -= 1
            elif event.key == SDLK_DOWN:
                is_key_pressing -= 1

    pass


def update():
    global is_key_pressing, bullet_dir, gusher, bullet, is_bullet_shot
    is_bullet_shot = False
    for game_object in game_world.all_objects():
        game_object.update()
    if is_key_pressing >= 1:
        bullet = Bullet(isaac.x, isaac.y, bullet_dir)
        game_world.add_object(bullet, 1)
        is_bullet_shot = True
    pass


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    delay(0.15)
    update_canvas()
    pass

