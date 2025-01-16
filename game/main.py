import pygame
from utils import scale_img
import car


pygame.init()

# Get information about the display
info = pygame.display.Info()
screen_width = info.current_w
screen_height = info.current_h

# Game Assets loading
GRASS = scale_img(pygame.image.load("imgs/grass.jpg"), 2.5)
TRACK = scale_img(pygame.image.load("imgs/track.png"), 0.75)
TRACK_BORDER = scale_img(pygame.image.load("imgs/track-border.png"), 0.75)
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)
FINISH_LINE = scale_img(pygame.image.load("imgs/finish.png"),0.8)
FINISH_LINE_POSITION = (110, 200)
FINISH_LINE_MASK = pygame.mask.from_surface(FINISH_LINE)
RED_CAR = scale_img(pygame.image.load("imgs/red-car.png"), 0.55)
GREEN_CAR = pygame.image.load("imgs/green-car.png")

# Game Window(surface) initialization
WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Driving Sim")


# Game config
FPS = 60
clock = pygame.time.Clock()
game_objects = [(GRASS, (0,0)), (TRACK, (0,0)), (FINISH_LINE, FINISH_LINE_POSITION), (TRACK_BORDER, (0,0))]
player_car = car.Car(RED_CAR, 5, 5, 150, 250)

# Game loop
run = True

def draw_objects(window: pygame.Surface, objects, car: car.Car):
    for obj, pos in objects:
        window.blit(obj, pos)
    car.draw(window)
    # Update the game each iteration
    pygame.display.update()


while run:
    # Limit clock to 60 fps, ensure all machine run the game on the same speed
    clock.tick(FPS)
    draw_objects(WINDOW, game_objects, player_car)

    # Event check
    for event in pygame.event.get():
        # Stop the game if game window exit button was clicked
        if event.type == pygame.QUIT:
            run = False
            break

    # key pressed
    player_car.update_car_movement()

    # check for collision
    if player_car.collide(TRACK_BORDER_MASK):
        player_car.bounce()
    
    finish_line_poi = player_car.collide(FINISH_LINE_MASK, *FINISH_LINE_POSITION)
    if finish_line_poi:
        if finish_line_poi[1] == 0:
            player_car.bounce()
        else:
            print("You win!")
            player_car.reset_position()


# Game termination
pygame.quit()