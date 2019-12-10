import game_framework
from pico2d import *
import boss_state
import game_world
name = "BossIntroState"
image = None
logo_time = 0.0
BackGround_Width = 1280
BackGround_Height = 960


def enter():
    global image
    game_world.objects = [[],[]]

    image = load_image('resource/BossIntro.png')
    pass


def exit():
    global image
    del(image)
    global BackGround_Width, BackGround_Height

    pass


def update():
    global logo_time
    if (logo_time >1.0):
        logo_time  = 0
        game_framework.change_state(boss_state)
    delay(0.01)
    logo_time += 0.01
    pass


def draw():
    global image
    clear_canvas()
    image.draw(BackGround_Width//2, BackGround_Height//2)
    update_canvas()
    pass




def handle_events():
    events = get_events()
    pass


def pause(): pass


def resume(): pass




