from pico2d import *
import random

BackGround_Width = 1280
BackGround_Height = 960


# Game object class here
class BackGround:
    def __init__(self):
        self.image = load_image('BackGround.png')

    def draw(self):
        self.image.draw(BackGround_Width//2, BackGround_Height//2)


class IssacHead:
    def __init__(self):
        self.x, self.y = BackGround_Width//2, BackGround_Height//2
        self.frame = 0
        self.image = load_image('isaac_head.png')

    def update(self):
        self.frame = (self.frame+1) % 2
        self.x += dir

    def draw(self):
        self.image.clip_draw(self.frame*80, 0, 80, 80, self.x, self.y)
    pass


class IssacBody:
    def __init__(self):
        self.x, self.y = BackGround_Width//2-5, (BackGround_Height//2)-50
        self.frame = 0
        self.image = load_image('isaac_body.png')

    def update(self):
        self.frame = (self.frame+1) % 8
        self.x += dir

    def draw(self):
        self.image.clip_draw(105*self.frame, 100, 60, 60, self.x, self.y)


def handle_events():
    global running
    global dir
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                dir += 1
            elif event.key == SDLK_LEFT:
                dir -= 1
            elif event.key == SDLK_ESCAPE:
                running = False
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                dir -= 1
            elif event.key == SDLK_LEFT:
                dir += 1


# initialization code
open_canvas(BackGround_Width, BackGround_Height)
running = True
character_head = IssacHead()
character_body = IssacBody()
background = BackGround()
# game main loop code
while running:
    handle_events()

    character_head.update()
    character_body.update()
    clear_canvas()

    background.draw()

    character_body.draw()
    delay(0.01)
    character_head.draw()
    delay(0.15)
    update_canvas()


# finalization code
close_canvas()