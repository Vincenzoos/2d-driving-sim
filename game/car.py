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
    
    def get_center_position(self):
        center_x = self.x + self.img.get_width() / 2
        center_y = self.y + self.img.get_height() / 2
        return center_x, center_y
    
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

    def collide(self, mask: pygame.Mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        intersection_point = mask.overlap(car_mask, offset)
        return intersection_point
    
    def reset_position(self):
        self.x = 150
        self.y = 150
        self.vel = 0
        self.angle = 0

    def draw_radar(self, window: pygame.Surface, mask: pygame.Mask):
        radar_angle = 90
        max_length = 200
        length = 0
        center_x, center_y = self.get_center_position()
        radar_x = int(center_x)
        radar_y = int(center_y)
        while mask.get_at((radar_x, radar_y)) ==0 and length < max_length:
            length += 1
            radar_x = center_x + length * math.cos(math.radians(self.angle + radar_angle))
            radar_y = center_y - length * math.sin(math.radians(self.angle + radar_angle))
        
        pygame.draw.line(window, (255, 255, 255), (center_x, center_y), (radar_x, radar_y), 1)
        pygame.draw.circle(window, (0,255,0), (radar_x, radar_y), 3)