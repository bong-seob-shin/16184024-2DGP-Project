import random
import json
import os

from pico2d import *
import game_world
import game_framework
import pause_state
import main_state
from Bullet import Bullet
from BackGround import BackGround
from Door import Door, InDoor
from Isaac import Isaac
from EnemyBullet_BigFly import EnemyBulletBigFly
import main_state_3
from Gaper import  Gaper
from Maggot import Maggot
from Health import Health
import death_state

BackGround_Width = 1280
BackGround_Height = 960
door_position = [(130), (1150)]

name = "MainState_3"

character_head = None
character_body = None
background = None
font = None
bullet = None


def enter():
    global isaac, background, is_key_pressed, is_attack_key_pressing, bullet_dir, gushers, is_bullet_create
    global BackGround_Width, BackGround_Height, invincibility_time, shot_term, bullets, door, indoor, monster_count
    global  flies, enemy_bullets, is_enemy_bullet_create,gapers , mulligans, maggotes
    game_world.objects = [[], []]
    BackGround_Width = 1280
    BackGround_Height = 960
    isaac = Isaac()
    isaac.x = 200
    isaac.y = BackGround_Height//2
    isaac.body_x, isaac.body_y = isaac.x - 5, isaac.y - 50
    isaac.velocity_x = main_state_3.isaac.velocity_x
    isaac.velocity_y = main_state_3.isaac.velocity_y
    isaac.now_health = main_state_3.hp
    monster_count = 7
    background = BackGround()
    door = Door()
    door.x = door_position[1]
    entrance_door = Door()
    entrance_door.x = door_position[0]
    indoor = InDoor()
    indoor.x = door_position[1]
    entrance_indoor = InDoor()
    entrance_indoor.x = door_position[0]
    gapers = [Gaper() for i in range(4)]
    maggotes = [Maggot() for i in range (3)]

    game_world.add_object(background,0)
    game_world.add_object(indoor, 1)
    game_world.add_object(door, 1)
    game_world.add_object(isaac, 1)
    game_world.add_object(entrance_door, 1)
    game_world.add_object(entrance_indoor, 1)
    game_world.add_objects(maggotes,1)
    game_world.add_objects(gapers, 1)
    is_key_pressed = 0
    is_attack_key_pressing = 0
    bullet_dir = 0
    is_bullet_create = False
    is_enemy_bullet_create = False
    invincibility_time = 0
    shot_term = 0

    bullets = []
    enemy_bullets = []
    pass


def exit():

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



def get_isaac():
    return isaac


def update():
    global is_attack_key_pressing, bullet_dir, gushers, bullet, is_bullet_create, invincibility_time, shot_term
    global flies, monster_count, indoor, enemy_bullets,bullets, is_enemy_bullet_create, mulligans
    global gapers,maggotes
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

            shot_term = 3
            is_bullet_create = True

    for gaper in gapers:
        if gaper.is_shot:
            if gaper.shot_term == 0:
                if not is_enemy_bullet_create:
                    enemy_bullet = EnemyBulletBigFly(gaper.x, gaper.y, gaper.dir)
                    game_world.add_object(enemy_bullet, 1)
                    enemy_bullets = [enemy_bullet]
                else:
                    enemy_bullet = EnemyBulletBigFly(gaper.x, gaper.y, gaper.dir)
                    game_world.add_object(enemy_bullet, 1)
                    enemy_bullets.append(enemy_bullet)
                is_enemy_bullet_create = True
                gaper.shot_term = 70

    for maggot in maggotes:
        for bullet in bullets:
            if collide(maggot, bullet):
                game_world.remove_object(bullet)
                bullets.remove(bullet)
                if maggot.health < 1:
                    maggotes.remove(maggot)
                    game_world.remove_object(maggot)
                    if monster_count > 0:
                        monster_count -= 1
                if maggot.health > 0:
                    maggot.health -= bullet.damage
                    print(maggot.health)



    if invincibility_time == 0:
        for maggot in maggotes:
            if collide(isaac, maggot):
                isaac.now_health -= 0.5
                invincibility_time = 10

        for gaper in gapers:
            if collide(isaac, gaper):
                isaac.now_health -= 0.5
                invincibility_time = 10

    for gaper in gapers:
        for bullet in bullets:
            if collide(gaper, bullet):
                game_world.remove_object(bullet)
                bullets.remove(bullet)
                if gaper.health < 1:
                    gapers.remove(gaper)
                    game_world.remove_object(gaper)
                    if monster_count > 0:
                        monster_count -= 1
                if gaper.health > 0:
                    gaper.health -= bullet.damage
                    print(gaper.health)




    if invincibility_time == 0:
            invincibility_time = 10
    if invincibility_time > 0:
        invincibility_time -= 1
    if shot_term >= 0:
        shot_term -= 1

    if monster_count == 0:
        indoor.open_door = True

    # if collide(isaac, indoor):
    #     if indoor.open_door:
    #         for game_object in game_world.all_objects():
    #              game_world.remove_object(game_object)
    #         game_framework.change_state(main_state_3)

    pass

    if isaac.is_death:
        game_framework.change_state(death_state)
def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    delay(0.15)
    update_canvas()
    pass

