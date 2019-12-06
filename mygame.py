import game_framework
import start_state
from pico2d import *


BackGround_Width = 1280
BackGround_Height = 960

# fill here
open_canvas(BackGround_Width, BackGround_Height)
game_framework.run(start_state)
close_canvas()