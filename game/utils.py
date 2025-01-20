import pygame
def scale_img(img: pygame.Surface, ratio: float) -> pygame.Surface:
    """
    Scales an image by a given ratio.

    Args:
        img (pygame.Surface): The image to be scaled.
        ratio (float): The scaling factor.

    Returns:
        pygame.Surface: The scaled image with updated dimensions.
    """
    size = round(img.get_width() * ratio), round(img.get_height() * ratio)
    return pygame.transform.scale(img, size)

def blit_rotate_center(window: pygame.Surface, image: pygame.Surface, top_left: tuple, angle: int):
    """
    Rotates an image around its center and draws it on the game window.

    Args:
        window (pygame.Surface): The surface where the rotated image will be drawn.
        image (pygame.Surface): The image to be rotated and drawn.
        top_left (tuple[int, int]): The top-left position of the image before rotation.
        angle (int): The rotation angle in degrees ('+' for clockwise and '-' for anti-clockwise).
    """
    rotated_img = pygame.transform.rotate(image, angle)
    new_rect = rotated_img.get_rect(center = image.get_rect(topleft=top_left).center)
    window.blit(rotated_img, new_rect.topleft)