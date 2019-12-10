from pico2d import *
import main_state

BackGround_Width = 1280
BackGround_Height = 960


class BackGround:
    def __init__(self, sound_num = 0):
        self.sound_num = sound_num
        if self.sound_num == 0:
            self.bgm = load_music('sound/basementLoop.ogg')
        elif self.sound_num == 1:
            self.bgm = load_music('sound/bossFight.ogg')
        elif self.sound_num == 2:
            self.bgm = load_music('sound/death.ogg')

        self.image = load_image('resource/BackGround.png')
        self.bgm.repeat_play()
        self.bgm.set_volume(65)

    def update(self):

        pass

    def draw(self):
        self.image.draw(BackGround_Width//2, BackGround_Height//2)

