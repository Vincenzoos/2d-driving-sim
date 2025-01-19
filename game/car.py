import pygame
import math
from utils import blit_rotate_center
from asset import *
# 

class Car:
    # 
    def __init__(self, img: pygame.Surface, max_vel: int, rotation_vel: int, x: int, y: int) -> None:
        self.img = img
        self.max_vel = max_vel
        self.rotation_vel = rotation_vel
        self.x = x
        self.y = y
        self.vel = 0
        self.angle = 0
        self.acceleration = 0.1
        self.friction = 0.1
        self.alive = True
        

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

    def draw(self):
        blit_rotate_center(WINDOW, self.img, (self.x, self.y), self.angle)

    def decceleration(self):
        if self.vel > 0:
            self.vel = max(self.vel - self.friction, 0)
        if self.vel < 0:
            self.vel += self.friction
        self.move()
      
    def bounce(self):
        self.vel = - self.vel/1.5
        self.move()

    def check_collision(self, mask: pygame.Mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        intersection_point = mask.overlap(car_mask, offset)
        if intersection_point:
            self.alive = False
        
    
    def update_car_status(self, is_alive: bool):
        self.alive = is_alive
        print("car is dead")

    def is_alive(self):
       return self.alive
    
    def reset_position(self):
        self.x = 150
        self.y = 150
        self.vel = 0
        self.angle = 0

    
class mannualCar(Car):
    def __init__(self):
        super().__init__(RED_CAR, 5, 5, 150, 250)
    
    def mannual_drive(self):
        # Human control mode
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

    

class autonomousCar(Car):
    def __init__(self):
        super().__init__(GREEN_CAR, 5, 5, 140, 250)
        self.radar_angles = [-135, -45, 45, 90, 135]
        self.radars=[]

    def autonomous_drive(self):
        # Self driving mode
        self.radars.clear()
        self.move_foward()
        self.rotate()
        self.draw_radar(WINDOW, TRACK_BORDER_MASK)
        self.check_collision(TRACK_BORDER_MASK)
        self.get_radar_data()

    def draw_radar(self, window: pygame.Surface, mask: pygame.mask):
        for ray_angle in self.radar_angles:
            max_length = self.img.get_width()*3
            length = 0
            center_x, center_y = self.get_center_position()
            while length <= max_length:
                radar_x = int(center_x + length * math.cos(math.radians(self.angle + ray_angle)))
                radar_y = int(center_y - length * math.sin(math.radians(self.angle + ray_angle)))
                if mask.get_at((radar_x, radar_y)):
                    break
                length += 1
            
            # Draw the radar
            pygame.draw.line(window, (255, 255, 255), (center_x, center_y), (radar_x, radar_y), 1)
            pygame.draw.circle(window, (0,255,0), (radar_x, radar_y), 3)

            # Calculate distance between the center of the car and the tip of the radar's ray for each radar
            dist = int(math.sqrt((radar_x - center_x)**2 + (radar_y - center_y)**2))

            # Append the dist and angle info of each radar to radars list of the car 
            self.radars.append((ray_angle, dist))

    def get_radar_data(self):
        # return list pf dist from car center to tip of radar's ray for each data as inputs for AI agent
        inputs = [0, 0, 0, 0, 0]
        for i, radar in enumerate(self.radars):
            inputs[i] = int(radar[1])
        return inputs