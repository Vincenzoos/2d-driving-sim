from utils import scale_img
import pygame
# Game Assets loading
GRASS = scale_img(pygame.image.load("imgs/grass.jpg"), 2.5)
TRACK = scale_img(pygame.image.load("imgs/track.png"), 0.75)
TRACK_BORDER = scale_img(pygame.image.load("imgs/track-border.png"), 0.75)
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)
FINISH_LINE = scale_img(pygame.image.load("imgs/finish.png"),0.8)
FINISH_LINE_POSITION = (110, 200)
FINISH_LINE_MASK = pygame.mask.from_surface(FINISH_LINE)
RED_CAR = scale_img(pygame.image.load("imgs/red-car.png"), 0.55)
GREEN_CAR = scale_img(pygame.image.load("imgs/green-car.png"), 0.55)


# Game Window(surface) initialization
WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Driving Sim")