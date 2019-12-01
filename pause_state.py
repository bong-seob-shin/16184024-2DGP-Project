import game_framework
from pico2d import *
import  game_world
import  main_state
import title_state
name = "PauseState"
image = None

def enter():
    global image
    image = load_image('resource/pause.png')
    pass


def exit():
    global image
    del(image)
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type,event.key) == (SDL_KEYDOWN,SDLK_SPACE):
            game_framework.change_state(title_state)
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.pop_state()
    pass


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    image.draw(main_state.BackGround_Width//2,main_state.BackGround_Height//2,1280, 960)

    update_canvas()
    pass







def update():
    pass


def pause():
    pass


def resume():
    pass
