from pico2d import *
import main_state

BackGround_Width = 1280
BackGround_Height = 960


RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, UP_DOWN, UP_UP, DOWN_UP, DOWN_DOWN, W_UP, W_DOWN, A_UP, A_DOWN, D_UP, D_DOWN, S_UP, S_DOWN = range(16)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYDOWN, SDLK_UP): UP_DOWN,
    (SDL_KEYDOWN, SDLK_DOWN): DOWN_DOWN,
    (SDL_KEYDOWN, SDLK_w): W_DOWN,
    (SDL_KEYDOWN, SDLK_a): A_DOWN,
    (SDL_KEYDOWN, SDLK_s): S_DOWN,
    (SDL_KEYDOWN, SDLK_d): D_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    (SDL_KEYUP, SDLK_UP): UP_UP,
    (SDL_KEYUP, SDLK_DOWN): DOWN_UP,
    (SDL_KEYUP, SDLK_w): W_UP,
    (SDL_KEYUP, SDLK_a): A_UP,
    (SDL_KEYUP, SDLK_s): S_UP,
    (SDL_KEYUP, SDLK_d): D_UP,
}


# Boy States

class IdleState:

    @staticmethod
    def enter(isaac, event):
        if event == RIGHT_DOWN:
            isaac.dir_x += 1
        elif event == LEFT_DOWN:
            isaac.dir_x -= 1
        elif event == RIGHT_UP:
            isaac.dir_x -= 1
        elif event == LEFT_UP:
            isaac.dir_x += 1

    @staticmethod
    def exit(isaac, event):
        # fill here
        pass

    @staticmethod
    def do(isaac):
        pass

    @staticmethod
    def draw(isaac):
        isaac.image.clip_draw(isaac.frame*80+isaac.left, 0, 80, 80, isaac.x, isaac.y)
        isaac.body_image.clip_draw(105 * isaac.body_frame, isaac.body_bottom, 60, 60, isaac.body_x, isaac.body_y)

class RunState:

    @staticmethod
    def enter(isaac, event):
        if event == RIGHT_DOWN:
            isaac.dir_x += 1
        elif event == LEFT_DOWN:
            isaac.dir_x -= 1
        elif event == RIGHT_UP:
            isaac.dir_x -= 1
        elif event == LEFT_UP:
            isaac.dir_x += 1

    @staticmethod
    def exit(isaac, event):
        # fill here
        pass

    @staticmethod
    def do(isaac):
        isaac.frame = (isaac.frame + 1) % 8
        isaac.x += isaac.dir_x
        isaac.x = clamp(25, isaac.x, 1280 - 25)

    @staticmethod
    def draw(isaac):
        isaac.image.clip_draw(isaac.frame*80+isaac.left, 0, 80, 80, isaac.x, isaac.y)
        isaac.body_image.clip_draw(105 * isaac.body_frame, isaac.body_bottom, 60, 60, isaac.body_x, isaac.body_y)


next_state_table = {
    IdleState: {RIGHT_UP: RunState, LEFT_UP: RunState,
                RIGHT_DOWN: RunState, LEFT_DOWN: RunState,
                UP_UP: RunState, DOWN_UP: RunState,
                UP_DOWN: RunState, DOWN_DOWN: RunState},
    RunState: {RIGHT_UP: IdleState, LEFT_UP: IdleState,
               LEFT_DOWN: IdleState, RIGHT_DOWN: IdleState,
               UP_UP: IdleState, DOWN_UP: IdleState,
               UP_DOWN: IdleState, DOWN_DOWN: IdleState},
    }

class Isaac:

    def __init__(self):
        self.x, self.y = BackGround_Width//2, BackGround_Height//2
        self.frame = 0
        self.image = load_image('isaac_head.png')
        self.dir_x = 0
        self.dir_y = 0
        self.left = 0
        self.body_x, self.body_y = self.x-5, self.y-50
        self.body_frame = 0
        self.body_image = load_image('isaac_body.png')
        self.body_is_move = False
        self.body_bottom = 90
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
        if self.body_is_move:
            self.body_frame = (self.body_frame+1) % 8
        if self.body_x > BackGround_Width-185:
            self.body_x = BackGround_Width-185
        elif self.body_x < 175:
            self.body_x = 175
        else:
            self.body_x += self.body_dir_x
        if self.body_y > BackGround_Height-200:
            self.body_y = BackGround_Height-200
        elif self.body_y < 170:
            self.body_y = 170
        else:
            self.body_y += self.body_dir_y


    def draw(self):
        self.image.clip_draw(self.frame*80+self.left, 0, 80, 80, self.x, self.y)
        self.body_image.clip_draw(105 * self.body_frame, self.body_bottom, 60, 60, self.body_x, self.body_y)
    pass
