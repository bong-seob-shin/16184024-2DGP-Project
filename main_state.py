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
from Door import  Door, InDoor
from Isaac import Isaac
from Rock import  Rock
import main_state_2
import death_state

from Health import Health


BackGround_Width = 1280
BackGround_Height = 960
door_position = [(130), (1150)]
name = "MainState"

character_head = None
character_body = None
background = None
font = None
bullet = None




def enter():
    global isaac, background, is_key_pressed , is_attack_key_pressing, bullet_dir, gushers, is_bullet_create
    global BackGround_Width, BackGround_Height, invincibility_time, shot_term, bullets, door, indoor, monster_count
    global rocks
    game_world.objects = [[], []]
    BackGround_Width = 1280
    BackGround_Height = 960
    isaac = Isaac()
    monster_count = 10
    gushers = [Gusher() for i in range (monster_count)]
    background = BackGround()
    door = Door()
    door.x = door_position[1]
    indoor = InDoor()
    indoor.x = door_position[1]
    rocks = [Rock(900, 400), Rock(900, 600), Rock(400, 400), Rock(400, 600)]
    game_world.add_object(background, 0)
    game_world.add_objects(rocks,0)
    game_world.add_object(indoor,1)
    game_world.add_object(door,1)
    game_world.add_object(isaac, 1)
    game_world.add_objects(gushers, 1)
    is_key_pressed = 0
    is_attack_key_pressing = 0
    bullet_dir = 0
    is_bullet_create = False
    invincibility_time = 0
    shot_term = 0
    bullets = []

    pass

def exit():
    global hp
    hp = isaac.now_health

    pass


def pause():
    pass


def resume():
    pass

def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False
    return True


def handle_events():
    global is_key_pressed
    global is_attack_key_pressing
    global bullet_dir
    global isaac

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.push_state(pause_state)
            elif event.key == SDLK_1:
                game_framework.change_state(main_state_2)
            elif event.key == SDLK_d:
                isaac.body_is_move = True
                isaac.velocity_x += isaac.velocity
                isaac.body_bottom = 0
                is_key_pressed += 1
            elif event.key == SDLK_a:
                isaac.body_is_move = True
                isaac.velocity_x -= isaac.velocity
                isaac.body_bottom = 180
                is_key_pressed += 1
            elif event.key == SDLK_w:
                isaac.body_is_move = True
                isaac.velocity_y += isaac.velocity
                isaac.body_bottom = 90
                is_key_pressed += 1
            elif event.key == SDLK_s:
                isaac.body_is_move = True
                isaac.velocity_y -= isaac.velocity
                isaac.body_bottom = 90
                is_key_pressed += 1
            elif event.key == SDLK_RIGHT:
                isaac.left = 160
                is_attack_key_pressing += 1
                bullet_dir = 0
            elif event.key == SDLK_LEFT:
                isaac.left = 480
                is_attack_key_pressing += 1
                bullet_dir = 1
            elif event.key == SDLK_UP:
                isaac.left = 320
                is_attack_key_pressing += 1
                bullet_dir = 2
            elif event.key == SDLK_DOWN:
                isaac.left = 0
                is_attack_key_pressing += 1
                bullet_dir = 3
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_d:
                is_key_pressed -= 1
                if is_key_pressed == 0:
                    isaac.body_is_move = False
                    isaac.body_frame = 0
                isaac.velocity_x -= isaac.velocity
            elif event.key == SDLK_a:
                is_key_pressed -= 1
                if is_key_pressed == 0:
                    isaac.body_is_move = False
                    isaac.body_frame = 0
                isaac.velocity_x += isaac.velocity
            elif event.key == SDLK_w:
                is_key_pressed -= 1
                if is_key_pressed == 0:
                    isaac.body_is_move = False
                    isaac.body_frame = 0
                isaac.velocity_y -= isaac.velocity
            elif event.key == SDLK_s:
                is_key_pressed -= 1
                if is_key_pressed == 0:
                    isaac.body_is_move = False
                    isaac.body_frame = 0
                isaac.velocity_y += isaac.velocity
            elif event.key == SDLK_RIGHT:
                is_attack_key_pressing -= 1
            elif event.key == SDLK_LEFT:
                is_attack_key_pressing -= 1
            elif event.key == SDLK_UP:
                is_attack_key_pressing -= 1
            elif event.key == SDLK_DOWN:
                is_attack_key_pressing -= 1

    pass


def update():
    global is_attack_key_pressing, bullet_dir, gushers, bullet, is_bullet_create,invincibility_time, shot_term, bullets
    global  gusher, monster_count, indoor, rocks, is_key_pressed
    for game_object in game_world.all_objects():
        game_object.update()

    if is_attack_key_pressing >= 1:
        if shot_term < 0:
            if not is_bullet_create:
                bullet = Bullet(isaac.x, isaac.y, bullet_dir)
                game_world.add_object(bullet, 1)
                bullets = [bullet]
            else:
                bullet = Bullet(isaac.x, isaac.y, bullet_dir)
                game_world.add_object(bullet, 1)
                bullets.append(bullet)

            shot_term = 30
            is_bullet_create = True

    for gusher in gushers:
        for bullet in bullets:
            if collide(gusher, bullet):
                game_world.remove_object(bullet)
                bullets.remove(bullet)
                if gusher.health < 1:
                    gushers.remove(gusher)
                    game_world.remove_object(gusher)
                    if monster_count>0:
                        monster_count -= 1
                if gusher.health > 0:
                    gusher.health -= bullet.damage
                    print(gusher.health)

    for rock in rocks:
        for bullet in bullets:
            if collide(rock, bullet):
                game_world.remove_object(bullet)
                bullets.remove(bullet)
        if collide(isaac, rock):
            if rock.x >= isaac.x :
                isaac.x -= isaac.velocity_x
                isaac.body_x -= isaac.velocity_x
            if rock.x <= isaac.x:
                isaac.x -= isaac.velocity_x
                isaac.body_x -= isaac.velocity_x
            if rock.y >= isaac.y:
                isaac.y -=isaac.velocity_y
                isaac.body_y -= isaac.velocity_y
            if rock.y <= isaac.y:
                isaac.y -=isaac.velocity_y
                isaac.body_y -=isaac.velocity_y
        for gusher in gushers:
           if collide(gusher, rock):
                if rock.x >= gusher.x :
                    gusher.x -= 10
                if rock.x <= gusher.x:
                    gusher.x += 10
                if rock.y >= gusher.y:
                    gusher.y -= 10
                if rock.y <= gusher.y:
                    gusher.y += 10


    if invincibility_time == 0:
        for gusher in gushers:
            if collide(isaac, gusher):
                isaac.now_health -= 0.5
                invincibility_time = 100
    if invincibility_time >0:
        invincibility_time -= 1
    if shot_term >=0:
        shot_term -= 1

    if monster_count == 0:
        indoor.open_door = True







    if collide(isaac, indoor):
        if indoor.open_door :
            game_framework.change_state(main_state_2)

    pass

    if isaac.is_death:

        game_framework.change_state(death_state)

def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()
    pass

