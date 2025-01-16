import pygame
import time
import math
from utils import scale_img
import car

# Game Assets loading
GRASS = scale_img(pygame.image.load("imgs/grass.jpg"), 2.5)
TRACK = scale_img(pygame.image.load("imgs/track.png"), 0.8)
TRACK_BORDER = scale_img(pygame.image.load("imgs/track-border.png"), 0.8)
FINISH_LINE = pygame.image.load("imgs/finish.png")
RED_CAR = scale_img(pygame.image.load("imgs/red-car.png"), 0.55)
GREEN_CAR = pygame.image.load("imgs/green-car.png")

# Game Window(surface) initialization
WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Driving Sim")


# Game config
FPS = 60
clock = pygame.time.Clock()
game_objects = [(GRASS, (0,0)), (TRACK, (0,0)), (TRACK_BORDER, (0,0))]
player_car = car.Car(RED_CAR, 5, 5, 170, 200)

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



# Game termination
pygame.quit()