from pico2d import *
import game_world

BackGround_Width = 1280
BackGround_Height = 960

class Health:

    image = None

    def __init__(self, x = 50):
        if Health.image == None:
            Health.image = load_image('resource/redheart.png')
        self.x = x
        self.y = BackGround_Height - 50
        self.heart_state = 0
        self.is_empty_heart = False
    def draw(self):
            self.image.clip_draw(60 * int(self.heart_state), 0, 60, 60, self.x, self.y)

    def update(self):
     pass