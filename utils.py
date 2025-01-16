import pygame
def scale_img(img: pygame.Surface, ratio: float) -> pygame.Surface:
    size = round(img.get_width() * ratio), round(img.get_height() * ratio)
    return pygame.transform.scale(img, size)

def blit_rotate_center(window: pygame.Surface, image: pygame.Surface, top_left, angle: int):
    rotated_img = pygame.transform.rotate(image, angle)
    new_rect = rotated_img.get_rect(center = image.get_rect(topleft=top_left).center)
    window.blit(rotated_img, new_rect.topleft)