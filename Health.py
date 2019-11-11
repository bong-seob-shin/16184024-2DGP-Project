from pico2d import *
import game_world

BackGround_Width = 1280
BackGround_Height = 960

class Health:

    image = None

    def __init__(self, x = 50):
        if Health.image == None:
            Health.image = load_image('resorce/redheart.png')
        self.x = x
        self.y = BackGround_Height - 50
        self.state_heart = 0

    def draw(self):
            self.image.clip_draw(60 * self.state_heart, 0, 60, 60, self.x, self.y)

    def update(self):
     pass