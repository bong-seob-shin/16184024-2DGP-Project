from pico2d import *


def handle_event():
    global running
    global x, y
    global dirx, diry
    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False



pass


BACKGROUND_WIDTH, BACKGROUND_HEIGHT = 1200, 485

open_canvas(BACKGROUND_WIDTH, BACKGROUND_HEIGHT)

back_ground = load_image('backGround01.png')
character01 = load_image('character01.png')
running = True

x = BACKGROUND_WIDTH // 2
y = BACKGROUND_HEIGHT // 2
while running:
    clear_canvas()
    back_ground.draw(BACKGROUND_WIDTH//2, BACKGROUND_HEIGHT//2)
    character01.clip_draw(80, 480, 80, 80, x, y)
    update_canvas()
    handle_event()
close_canvas()