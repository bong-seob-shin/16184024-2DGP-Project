import random
import json
import os

from pico2d import *
import game_world
import game_framework
import pause_state
import main_state_4
from Black_Bullet import  BlackBullet
from Bullet import Bullet
from BackGround import BackGround
from Door import Door, InDoor
from Isaac import Isaac
from Duke import Duke
from Fly_created_Boss import Fly
from BigFly_created_Boss import BigFly
from EnemyBullet import EnemyBulletBigFly
import death_state
import  title_state

BackGround_Width = 1280
BackGround_Height = 960
door_position = [(130)]

name = "BossState"

character_head = None
character_body = None
background = None
font = None
bullet = None


def enter():
    global isaac, background, is_key_pressed, is_attack_key_pressing, bullet_dir, gushers, is_bullet_create
    global BackGround_Width, BackGround_Height, invincibility_time, shot_term, bullets, door,  monster_count
    global  flies, big_flies, enemy_bullets, is_enemy_bullet_create, is_bullet_upgrade, is_black_bullet_create
    global duke,is_monster_create


    game_world.objects = [[],[]]
    BackGround_Width = 1280
    BackGround_Height = 960
    isaac = Isaac()
    isaac.x = 200
    isaac.y = BackGround_Height//2
    isaac.body_x, isaac.body_y = isaac.x - 5, isaac.y - 50
    isaac.now_health = main_state_4.hp
    isaac.body_is_move = False
    duke = Duke()
    monster_count = 0
    background = BackGround(1)
    entrance_door = Door()
    entrance_door.x = door_position[0]
    entrance_indoor = InDoor()
    entrance_indoor.x = door_position[0]

    game_world.add_object(background,0)
    game_world.add_object(isaac, 1)
    game_world.add_object(duke,1)
    game_world.add_object(entrance_door, 1)
    game_world.add_object(entrance_indoor, 1)
    is_key_pressed = 0
    is_attack_key_pressing = 0
    bullet_dir = 0
    is_bullet_create = False
    is_enemy_bullet_create = False
    is_bullet_upgrade = main_state_4.is_bullet_upgrade
    is_black_bullet_create = False
    is_monster_create = False
    invincibility_time = 100
    shot_term = 100
    flies = []
    big_flies = []
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
    global isaac,background

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
    global flies, monster_count, big_flies, enemy_bullets,bullets, is_enemy_bullet_create, enemy_big_fly_shot_term
    global  is_bullet_upgrade, is_black_bullet_create, duke, is_monster_create,background
    for game_object in game_world.all_objects():
        game_object.update()


    if duke.create_fly_timer == 0:
        if not is_monster_create:
            fly1 = Fly(duke.x,duke.y+10)
            fly2 = Fly(duke.x,duke.y-10)
            big_fly = BigFly(duke.x-10, duke.y)
            game_world.add_object(fly1,1)
            game_world.add_object(fly2,1)
            game_world.add_object(big_fly,1)
            flies = [fly1,fly2]
            big_flies = [big_fly]
        else:
            fly1 = Fly(duke.x, duke.y + 10)
            fly2 = Fly(duke.x, duke.y - 10)
            big_fly = BigFly(duke.x - 10, duke.y)
            game_world.add_object(fly1, 1)
            game_world.add_object(fly2, 1)
            game_world.add_object(big_fly, 1)
            flies.append(fly1)
            flies.append(fly2)
            big_flies.append(big_fly)
        is_monster_create= True
        duke.summon()
        duke.create_fly_timer = 500

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

    if is_bullet_upgrade:
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

    for big_fly in big_flies:
        if big_fly.is_shot:
            if big_fly.shot_term == 0:
                if not is_enemy_bullet_create:
                    enemy_bullet = EnemyBulletBigFly(big_fly.x, big_fly.y, big_fly.dir)
                    game_world.add_object(enemy_bullet, 1)
                    enemy_bullets = [enemy_bullet]
                else:
                    enemy_bullet = EnemyBulletBigFly(big_fly.x, big_fly.y, big_fly.dir)
                    game_world.add_object(enemy_bullet, 1)
                    enemy_bullets.append(enemy_bullet)
                is_enemy_bullet_create = True
                big_fly.shot_term = 200

    for fly in flies:
        for bullet in bullets:
            if collide(fly, bullet):
                game_world.remove_object(bullet)
                bullets.remove(bullet)
                if fly.health < 1:
                    flies.remove(fly)
                    game_world.remove_object(fly)
                    if monster_count > 0:
                        monster_count -= 1
                if fly.health > 0:
                    fly.health -= bullet.damage
                    print(fly.health)

    for bullet in bullets:
        if collide(duke, bullet):
            game_world.remove_object(bullet)
            bullets.remove(bullet)
            if duke.health < 1:
                game_world.remove_object(duke)
                game_framework.change_state(title_state)
            if duke.health >0 :
                duke.health -= bullet.damage
                print(duke.health)

    if invincibility_time == 0:
        for fly in flies:
            if collide(isaac, fly):
                isaac.now_health -= 0.5
                isaac.hurt()
                invincibility_time = 100
        for big_fly in big_flies:
            if collide(isaac, big_fly):
                isaac.now_health -= 0.5
                isaac.hurt()
                invincibility_time = 100
        for enemy_bullet in enemy_bullets:
            if collide(isaac, enemy_bullet):
                game_world.remove_object(enemy_bullet)
                enemy_bullets.remove(enemy_bullet)
                isaac.now_health -= enemy_bullet.damage
                isaac.hurt()
                invincibility_time = 100
        if collide(isaac, duke):
            isaac.now_health -= 1
            isaac.hurt()
            invincibility_time = 100

    for big_fly in big_flies:
        for bullet in bullets:
            if collide(big_fly, bullet):
                game_world.remove_object(bullet)
                bullets.remove(bullet)
                if big_fly.health < 1:
                    big_flies.remove(big_fly)
                    game_world.remove_object(big_fly)
                    if monster_count > 0:
                        monster_count -= 1
                if big_fly.health > 0:
                    big_fly.health -= bullet.damage
                    print(big_fly.health)





    if invincibility_time > 0:
        invincibility_time -= 1
    if shot_term >= 0:
        shot_term -= 1


    if duke.create_fly_timer > 0:
        duke.create_fly_timer -= 1

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

