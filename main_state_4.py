import random
import json
import os

from pico2d import *
import game_world
import game_framework
import pause_state
import main_state
import boss_intro_state
from Bullet import Bullet
from Black_Bullet import BlackBullet
from BackGround import BackGround
from Door import Door, InDoor
from Isaac import Isaac
from EnemyBullet import EnemyBulletBigFly
import main_state_3
from Gaper_stage_4 import  Gaper
from Maggot import Maggot
from Health import Health
import death_state
from Needle import  Needle
from Item import RecoveryHp, UpgradeBullet

BackGround_Width = 1280
BackGround_Height = 960
door_position = [(130), (1150)]

name = "MainState_3"

character_head = None
character_body = None
background = None
font = None
bullet = None
Needle.image = None

def enter():
    global isaac, background, is_key_pressed, is_attack_key_pressing, bullet_dir, gushers, is_bullet_create
    global BackGround_Width, BackGround_Height, invincibility_time, shot_term, bullets, door, indoor, monster_count
    global  flies, enemy_bullets, is_enemy_bullet_create,gapers , maggotes, needles, needle_up_timer
    global is_item_create,  is_bullet_upgrade, is_black_bullet_create ,is_eat_item , background
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
    monster_count = 10
    background = BackGround()
    door = Door()
    door.x = door_position[1]
    entrance_door = Door()
    entrance_door.x = door_position[0]
    indoor = InDoor()

    indoor.x = door_position[1]
    entrance_indoor = InDoor()
    entrance_indoor.x = door_position[0]
    needles = [Needle(360, 210),Needle(360, 275),Needle(360, 340),Needle(360, 400),Needle(360, 460), Needle(360, 520), Needle(360, 580), Needle(360, 640), Needle(360, 700), Needle(360, 760),
             Needle(560, 210),Needle(560, 275),Needle(560, 340),Needle(560, 400),Needle(560, 460), Needle(560, 520), Needle(560, 580), Needle(560, 640), Needle(560, 700), Needle(560, 760),
               Needle(760, 210),Needle(760, 275),Needle(760, 340),Needle(760, 400),Needle(760, 460), Needle(760, 520), Needle(760, 580), Needle(760, 640), Needle(760, 700), Needle(760, 760),
               Needle(960, 210),Needle(960, 275),Needle(960, 340),Needle(960, 400),Needle(960, 460), Needle(960, 520), Needle(960, 580), Needle(960, 640), Needle(960, 700), Needle(960, 760),]
    gapers = [Gaper() for i in range(5)]
    maggotes = [Maggot() for i in range (5)]

    game_world.add_object(background,0)
    game_world.add_objects(needles, 0)
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
    is_item_create = False
    is_bullet_upgrade = False
    is_black_bullet_create = False
    invincibility_time = 100
    shot_term = 0
    needle_up_timer= 200
    is_eat_item = False
    bullets = []
    enemy_bullets = []
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
def collide_ex(a,b):
    left_a, bottom_a, right_a, top_a = a.body_get_bb()
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
    global isaac,background,monster_count

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.push_state(pause_state)
            elif event.key == SDLK_1:
                game_framework.change_state(boss_intro_state)
            elif event.key == SDLK_0:
                monster_count = 0
                for gaper in gapers:
                    game_world.remove_object(gaper)
                    gapers.remove(gaper)
                for maggot in maggotes:
                    game_world.remove_object(maggot)
                    maggotes.remove(maggot)
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
    global gapers, maggotes, needles, needle_up_timer, recovery_hp, upgrade_bullet, is_item_create,is_bullet_upgrade
    global is_black_bullet_create, is_eat_item,background
    for game_object in game_world.all_objects():
        game_object.update()

    if not is_bullet_upgrade:
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

    if  is_bullet_upgrade:
        if is_attack_key_pressing >= 1:
            if shot_term < 0:

                if not is_black_bullet_create:
                    bullet = BlackBullet(isaac.x, isaac.y, bullet_dir)
                    game_world.add_object(bullet, 1)
                    bullets = [bullet]
                else:
                    bullet = BlackBullet(isaac.x, isaac.y, bullet_dir)
                    game_world.add_object(bullet, 1)
                    bullets.append(bullet)
                shot_term = 30
                is_black_bullet_create = True

    for gaper in gapers:
        if gaper.is_shot:
            if gaper.shot_term == 0:
                if not is_enemy_bullet_create:
                    enemy_bullet = EnemyBulletBigFly(gaper.x, gaper.y, gaper.dir,3)
                    game_world.add_object(enemy_bullet, 1)
                    enemy_bullets = [enemy_bullet]
                else:
                    enemy_bullet = EnemyBulletBigFly(gaper.x, gaper.y, gaper.dir,3)
                    game_world.add_object(enemy_bullet, 1)
                    enemy_bullets.append(enemy_bullet)
                is_enemy_bullet_create = True
                gaper.shot_term = 200

    if is_enemy_bullet_create:
        for enemy_bullet in enemy_bullets:
            if enemy_bullet.is_delete:
                enemy_bullets.remove(enemy_bullet)

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


    if needle_up_timer < 0:
        needle_up_timer = 200
        for needle in needles:
            needle.change_needle_state()

    if invincibility_time == 0:
        for maggot in maggotes:
            if collide(isaac, maggot):
                isaac.now_health -= 0.5
                isaac.hurt()
                invincibility_time = 100

        for gaper in gapers:
            if collide(isaac, gaper):
                isaac.now_health -= 0.5
                isaac.hurt()
                invincibility_time = 100

        for needle in needles:
            if needle.needle_up:
                if collide_ex(isaac, needle):
                    isaac.now_health -= needle.damage
                    isaac.hurt()
                    invincibility_time = 100

        for enemy_bullet in enemy_bullets:
            if collide(isaac, enemy_bullet):
                game_world.remove_object(enemy_bullet)
                enemy_bullets.remove(enemy_bullet)
                isaac.now_health -= enemy_bullet.damage
                isaac.hurt()
                invincibility_time = 100

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





    if invincibility_time > 0:
        invincibility_time -= 1
    if shot_term >= 0:
        shot_term -= 1

    if needle_up_timer >= 0:
        needle_up_timer -=1



    if monster_count == 0:
        if not indoor.open_door:
            indoor.open()
        indoor.open_door = True


        if not is_item_create:
            recovery_hp = RecoveryHp()
            upgrade_bullet = UpgradeBullet()
            game_world.add_object(upgrade_bullet, 1)
            game_world.add_object(recovery_hp, 1)
            is_item_create = True

    if is_item_create:
        if not is_eat_item:
            if collide(isaac, recovery_hp):
                game_world.remove_object(upgrade_bullet)
                game_world.remove_object(recovery_hp)
                isaac.eat_health_item()
                isaac.now_health = 3
                is_eat_item = True
            if collide(isaac, upgrade_bullet):
                game_world.remove_object(upgrade_bullet)
                game_world.remove_object(recovery_hp)
                isaac.eat_upgrade_bullet_item()
                is_bullet_upgrade = True
                is_eat_item = True


    if collide(isaac, indoor):
        if indoor.open_door:
            for game_object in game_world.all_objects():
                 game_world.remove_object(game_object)
            game_framework.change_state(boss_intro_state)
            background.bgm.stop()
            indoor.enter_boss_room()

    pass

    if isaac.is_death:
        game_world.remove_object(background)
        background = BackGround(2)
        game_world.add_object(background, 0)
        game_framework.change_state(death_state)
def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()
    pass

