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


def handle_events():
    global running
    global is_key_pressed
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
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
            elif event.key == SDLK_LEFT:
                character_head.left = 480
            elif event.key == SDLK_UP:
                character_head.left = 320
            elif event.key == SDLK_DOWN:
                character_head.left = 0
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



# initialization code
open_canvas(BackGround_Width, BackGround_Height)
running = True
character_head = IssacHead()
character_body = IssacBody()
background = BackGround()
is_key_pressed = 0
# game main loop code
while running:
    handle_events()

    character_head.update()
    character_body.update()
    clear_canvas()

    background.draw()

    character_body.draw()
    character_head.draw()
    delay(0.15)
    update_canvas()


# finalization code
close_canvas()