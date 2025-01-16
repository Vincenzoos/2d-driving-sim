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

    def move_backword(self):
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

        
