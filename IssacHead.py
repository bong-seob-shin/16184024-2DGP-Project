
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
