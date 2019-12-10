from pico2d import *
import main_state


class RecoveryHp:
    def __init__(self):
        self.image = load_image('resource/Recovery_Hp.png')
        self.x = 200
        self.y = main_state.BackGround_Height//2 + 150
    def update(self):
        pass

    def draw(self):
         self.image.draw(self.x, self.y)

    def get_bb(self):
        return self.x - 40, self.y - 40, self.x + 40, self.y + 40



class UpgradeBullet:
    def __init__(self):
        self.image = load_image('resource/Upgrade_Bullet.png')
        self.x = 200
        self.y = main_state.BackGround_Height//2 - 150
    def update(self):

        pass

    def draw(self):
        self.image.draw(self.x, self.y)

    def get_bb(self):
        return self.x - 40, self.y - 40, self.x + 40, self.y + 40


