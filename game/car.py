import pygame
import math
from utils import blit_rotate_center
# 
class Car:
    # 
    def __init__(self, img: pygame.Surface, max_vel: int, rotation_vel: int, x: int, y: int) -> None:
        self.img = img
        self.max_vel = max_vel
        self.rotation_vel = rotation_vel
        self.vel = 0
        self.angle = 0
        self.x = x
        self.y = y
        self.acceleration = 0.1
        self.friction = 0.1

    def rotate(self, left=False, right=False) -> None:
        if left:
            self.angle += self.rotation_vel
        if right:
            self.angle -= self.rotation_vel
    
    def move_foward(self):
        # Never exceeds max vel
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move_backward(self):
        # Never exceeds max vel
        self.vel = max(self.vel - self.acceleration, -self.max_vel/2)
        self.move()
    
    def move(self):
        # Note that the unit circle was rotated 90 deg since the car at angle 0 is [^]
        angle_rad = math.radians(self.angle)
        vertical_displacement = math.cos(angle_rad) * self.vel
        horizontal_displacement = math.sin(angle_rad) * self.vel

        self.x -= horizontal_displacement
        self.y -= vertical_displacement

    def draw(self, window: pygame.Surface):
        blit_rotate_center(window, self.img, (self.x, self.y), self.angle)

    def decceleration(self):
        if self.vel > 0:
            self.vel = max(self.vel - self.friction, 0)
        if self.vel < 0:
            self.vel += self.friction
        self.move()
    
    def update_car_movement(self):
        moved = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rotate(left=True)
        if keys[pygame.K_d]:
            self.rotate(right=True)
        if keys[pygame.K_w]:
            moved = True
            self.move_foward()
        if keys[pygame.K_s]:
            moved = True
            self.move_backward()

        if not moved:
            self.decceleration()
    
    def bounce(self):
        self.vel = - self.vel/1.5
        self.move()

    def check_collision(self, mask: pygame.Mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        intersection_point = mask.overlap(car_mask, offset)
        if intersection_point != None:
            self.bounce()