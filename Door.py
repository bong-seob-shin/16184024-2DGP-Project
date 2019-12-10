from pico2d import *
import main_state

class Door:
    def __init__(self):
        self.image = load_image('resource/door.png')
        self.x = 0
        self.y = main_state.BackGround_Height//2
    def update(self):
        pass

    def draw(self):
        if self.x < main_state.BackGround_Width//2:
            self.image.composite_draw(0,'h',self.x,self.y)
        else:
            self.image.draw(self.x, self.y)



class InDoor():
    def __init__(self):
        self.image = load_image('resource/close_door.png')
        self.x = 0
        self.y = main_state.BackGround_Height//2
        self.open_sound = load_wav('sound/doorOpen.wav')
        self.open_sound.set_volume(32)
        self.open_door = False
        self.enter_boss_room_sound = load_wav('sound/bossEnter.wav')
        self.enter_boss_room_sound.set_volume(32)
    def update(self):
        if self.open_door:
            self.image = load_image('resource/open_door.png')
        pass

    def draw(self):
        if self.x < main_state.BackGround_Width // 2:
            self.image.composite_draw(0, 'h', self.x, self.y)
        else:
            self.image.draw(self.x, self.y)

    def get_bb(self):
        return self.x - 20, self.y - 40, self.x + 20, self.y + 40

    def open(self):
        self.open_sound.play()

    def enter_boss_room(self):
        self.enter_boss_room_sound.play()
