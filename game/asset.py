from utils import scale_img
import pygame
# Game Assets loading
# These assets include images for the game environment and vehicles, scaled to appropriate sizes for user-friendly window display dimension.
GRASS = scale_img(pygame.image.load("imgs/grass.jpg"), 2.5)
TRACK = scale_img(pygame.image.load("imgs/track.png"), 0.8)
TRACK_BORDER = scale_img(pygame.image.load("imgs/track-border.png"), 0.8)
FINISH_LINE = scale_img(pygame.image.load("imgs/finish.png"),0.8)
RED_CAR = scale_img(pygame.image.load("imgs/red-car.png"), 0.45)
GREEN_CAR = scale_img(pygame.image.load("imgs/green-car.png"), 0.45)

FINISH_LINE_POSITION = (110, 200)
# Mask for collision detection with track border
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)

# Mask for detecting crossing the finish line
FINISH_LINE_MASK = pygame.mask.from_surface(FINISH_LINE)

# Game Window set up
# Setting up the game window dimensions and properties based on the track image dimensions.
WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Driving Sim")