import game_framework
from pico2d import *
import main_state
import  game_world
name = "TitleState"
image = None


def enter():
    global image, BackGround_Width, BackGround_Height
    image = load_image('resorce/title1.png')
    BackGround_Width = 1280
    BackGround_Height = 960
    game_world.objects = [[], []]
    pass


def exit():
    global image, BackGround_Width, BackGround_Height
    del(image)
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit

            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                game_framework.change_state(main_state)
    pass


def draw():
    clear_canvas()
    image.draw(BackGround_Width//2, BackGround_Height//2)
    update_canvas()
    pass







def update():
    pass


def pause():
    pass


def resume():
    pass






