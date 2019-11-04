import random
import json
import os

from pico2d import *
import game_world
import game_framework
import pause_state
import random

BackGround_Width = 1280
BackGround_Height = 960

name = "MainState"

character_head = None
character_body = None
background = None
font = None
bullet = None


class Gusher:
    image = None

    def __init__(self):
        if Gusher.image == None:
            Gusher.image = load_image('Gusher.png')
        self.x = BackGround_Width//2 + 100
        self.y = BackGround_Height//2
        self.velocity = 20
        self.dir = 1
        self.timer = 5

    def update(self):
        self.timer -= 1
        if self.timer == 0:
            self.dir = random.randint(1, 4)
            self.timer = 5
        if self.dir == 1 :
           self.x = self.x + self.velocity
        elif self.dir == 2:
            self.x = self.x - self.velocity
        elif self.dir == 3:
            self.y = self.y + self.velocity
        elif self.dir == 4:
            self.y = self.y - self.velocity

        if self.x > BackGround_Width-180:
            self.x = BackGround_Width-180
        elif self.x < 180:
            self.x = 180
        if self.y > BackGround_Height-150:
            self.y = BackGround_Height-150
        elif self.y < 220:
            self.y = 220

    def draw(self):
        self.image.draw(self.x, self.y, 100, 100)

    pass

def is_crashed(Bullet, Gusher):
    if Bullet.x == Gusher.x:
        if Bullet.y == Gusher.y:
            game_world.remove_object(Gusher)
            game_world.remove_object(Bullet)

class Bullet:

    image = None

    def __init__(self, x = 400, y= 300, b_dir =0):
        if Bullet.image == None:
            Bullet.image = load_image('bullet.png')
        self.x, self.y, self.b_dir = x, y, b_dir
        self.velocity = 40
        self.start_x = self.x
        self.start_y = self.y
    def draw(self):
        if self.b_dir == 0: #오른쪽
            self.image.draw(self.x+40, self.y)
        elif self.b_dir == 1: #왼쪽
            self.image.draw(self.x-40, self.y)
        elif self.b_dir == 2: #아래
            self.image.draw(self.x, self.y+40)
        elif self.b_dir == 3: #위
            self.image.draw(self.x, self.y-40)

    def update(self):
        if self.b_dir == 0: #오른쪽
            if self.x > self.start_x+300:
                self.y -= 10

                if self.velocity> 10:
                    self.velocity -= 8
            self.x += self.velocity
        elif self.b_dir == 1: #왼쪽
            if self.x < self.start_x-300:
                self.y -= 10
                if self.velocity > 10:
                    self.velocity -= 8
            self.x -= self.velocity
        elif self.b_dir == 2: #아래
            self.y += self.velocity
        elif self.b_dir == 3: #위
            self.y -= self.velocity

        if self.x < 175 or self.x > 1280 - 175:
            game_world.remove_object(self)
        elif self.x > self.start_x+400 or self.x < self.start_x-400:
            game_world.remove_object(self)

        if self.y < 155 or self.y > 960 - 150:
            game_world.remove_object(self)
        elif self.y <self.start_y - 400 or self.y > self.start_y+400:
            game_world.remove_object(self)
    pass


class BackGround:
    def __init__(self):
        self.image = load_image('BackGround.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(BackGround_Width//2, BackGround_Height//2)


class IssacHead:

    def __init__(self):
        self.x, self.y = BackGround_Width//2, BackGround_Height//2
        self.frame = 0
        self.image = load_image('isaac_head.png')
        self.dir_x = 0
        self.dir_y = 0
        self.left = 0
    def update(self):
        self.frame = (self.frame+1) % 2
        if self.x > BackGround_Width-180:
            self.x = BackGround_Width-180
        elif self.x < 180:
            self.x = 180
        else:
            self.x += self.dir_x
        if self.y > BackGround_Height-150:
            self.y = BackGround_Height-150
        elif self.y < 220:
            self.y = 220
        else:
            self.y += self.dir_y
    def draw(self):
        self.image.clip_draw(self.frame*80+self.left, 0, 80, 80, self.x, self.y)
    pass


class IssacBody:

    def __init__(self):
        self.x, self.y = BackGround_Width//2-5, (BackGround_Height//2)-50
        self.frame = 0
        self.image = load_image('isaac_body.png')
        self.dir_x = 0
        self.dir_y = 0
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
            self.x += self.dir_x
        if self.y > BackGround_Height-200:
            self.y = BackGround_Height-200
        elif self.y < 170:
            self.y = 170
        else:
            self.y += self.dir_y

    def draw(self):
        self.image.clip_draw(105*self.frame, self.bottom, 60, 60, self.x, self.y)




def enter():
    global character_head, character_body, background, is_key_pressed , is_key_pressing, bullet_dir, gusher
    global BackGround_Width, BackGround_Height
    BackGround_Width = 1280
    BackGround_Height = 960
    character_head = IssacHead()
    character_body = IssacBody()
    gusher = Gusher()
    background = BackGround()
    game_world.add_object(background, 0)
    game_world.add_object(character_body, 1)
    game_world.add_object(character_head, 1)
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
                character_body.is_move = True
                character_head.dir_x += 20
                character_body.dir_x += 20
                character_body.bottom = 0
                is_key_pressed += 1
            elif event.key == SDLK_a:
                character_body.is_move = True
                character_head.dir_x -= 20
                character_body.dir_x -= 20
                character_body.bottom = 180
                is_key_pressed += 1
            elif event.key == SDLK_w:
                character_body.is_move = True
                character_head.dir_y += 20
                character_body.dir_y += 20
                character_body.bottom = 90
                is_key_pressed += 1
            elif event.key == SDLK_s:
                character_body.is_move = True
                character_head.dir_y -= 20
                character_body.dir_y -= 20
                character_body.bottom = 90
                is_key_pressed += 1
            elif event.key == SDLK_RIGHT:
                character_head.left = 160
                is_key_pressing += 1
                bullet_dir = 0
            elif event.key == SDLK_LEFT:
                character_head.left = 480
                is_key_pressing += 1
                bullet_dir = 1
            elif event.key == SDLK_UP:
                character_head.left = 320
                is_key_pressing += 1
                bullet_dir = 2
            elif event.key == SDLK_DOWN:
                character_head.left = 0
                is_key_pressing += 1
                bullet_dir = 3
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_d:
                is_key_pressed -= 1
                if is_key_pressed == 0:
                    character_body.is_move = False
                    character_body.frame = 0
                character_head.dir_x -= 20
                character_body.dir_x -= 20
            elif event.key == SDLK_a:
                is_key_pressed -= 1
                if is_key_pressed == 0:
                    character_body.is_move = False
                    character_body.frame = 0
                character_head.dir_x += 20
                character_body.dir_x += 20
            elif event.key == SDLK_w:
                is_key_pressed -= 1
                if is_key_pressed == 0:
                    character_body.is_move = False
                    character_body.frame = 0
                character_head.dir_y -= 20
                character_body.dir_y -= 20
            elif event.key == SDLK_s:
                is_key_pressed -= 1
                if is_key_pressed == 0:
                    character_body.is_move = False
                    character_body.frame = 0
                character_head.dir_y += 20
                character_body.dir_y += 20
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
        bullet = Bullet(character_head.x, character_head.y, bullet_dir)
        game_world.add_object(bullet, 1)
        is_bullet_shot = True
    if is_bullet_shot == True:
        is_crashed(bullet, gusher)
    pass


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    delay(0.15)
    update_canvas()
    pass





