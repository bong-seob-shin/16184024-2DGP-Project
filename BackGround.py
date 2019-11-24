from pico2d import *
import main_state

BackGround_Width = 1280
BackGround_Height = 960


class BackGround:
    def __init__(self):
        self.image = load_image('resorce/BackGround.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(BackGround_Width//2, BackGround_Height//2)

