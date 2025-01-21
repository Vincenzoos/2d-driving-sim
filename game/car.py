import pygame
import math
from utils import blit_rotate_center
from asset import *

"""
Car: Represents a generic car with basic properties such as position, velocity, rotation,
and methods to handle movement, collisions, and rendering.
"""
class Car:
    def __init__(self, img: pygame.Surface, max_vel: int, rotation_vel: int, x: int, y: int):
        """
        Initializes the generic Car object with core attributes image, max velocity, rotation velocity, position, etc.

        Attributes:
            img (pygame.Surface): The image representing the car.
            max_vel (int): The maximum velocity of the car.
            rotation_vel (int): The rotational velocity of the car.
            x (int): The x-coordinate of the car's position.
            y (int): The y-coordinate of the car's position.
            vel (float): The current velocity of the car.
            angle (float): The current angle of the car.
            acceleration (float): The rate of acceleration for the car.
            friction (float): The rate of deceleration for the car.
            alive (bool): Indicates whether the car is still active (not crashed).
        """
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
        

    def rotate(self, left=False, right=False):
        """
        Rotates the car by adjusting its angle.

        Args:
            left (bool): If True, rotates the car counterclockwise.
            right (bool): If True, rotates the car clockwise.
        """
        if left:
            self.angle += self.rotation_vel
        if right:
            self.angle -= self.rotation_vel
    
    def move_foward(self):
        """
        Moves the car forward by increasing its velocity, up to the maximum velocity.
        """
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move_backward(self):
        """
        Moves the car backward by decreasing its velocity, limited to half the maximum velocity in reverse.
        """
        self.vel = max(self.vel - self.acceleration, -self.max_vel/2)
        self.move()
    
    def get_center_position(self) -> tuple:
        """
        Calculates and returns the center point of the car.

        Returns:
            tuple: A tuple containing the (x, y) coordinates of the car's center.
        """
        center_x = self.x + self.img.get_width() / 2
        center_y = self.y + self.img.get_height() / 2
        return center_x, center_y
    
    def move(self):
        """
        Updates the car's position based on its velocity and angle.
        *Note that the unit circle was rotated 90 degree anti-clockwise since the car at angle 0 is [^]*
        """
        angle_rad = math.radians(self.angle)
        vertical_displacement = math.cos(angle_rad) * self.vel
        horizontal_displacement = math.sin(angle_rad) * self.vel

        self.x -= horizontal_displacement
        self.y -= vertical_displacement

    def draw(self):
        """
        Draws the car on the screen at its current position and angle.
        """
        blit_rotate_center(WINDOW, self.img, (self.x, self.y), self.angle)

    def decceleration(self):
        """
        Gradually reduces the car's velocity, simulating friction.
        """
        if self.vel > 0:
            self.vel = max(self.vel - self.friction, 0)
        if self.vel < 0:
            self.vel += self.friction
        self.move()
      
    def bounce(self):
        """
        Simulating a reaction force applied to the car upon collision with obstacles such as track border, forcing it to move in the opposite direction.
        """
        self.vel = - self.vel/1.5
        self.move()

    def check_collision(self, mask: pygame.Mask, x=0, y=0) -> tuple:
        """
        Checks for collision with another object represented by a mask, return collision point of there is one, otherwise return None.

        Args:
            mask (pygame.Mask): The mask to check collision against.
            x (int, optional): The x-coordinate of the mask's position. Defaults to 0.
            y (int, optional): The y-coordinate of the mask's position. Defaults to 0.
        """
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        intersection_point = mask.overlap(car_mask, offset)
        # if collision detected, set car alive status to False
        if intersection_point:
            self.alive = False
        return intersection_point
        
    
    def update_car_status(self, is_alive: bool):
        """
        Updates the car's status to alive or not.

        Args:
            is_alive (bool): The updated status of the car.
        """
        self.alive = is_alive
        print("car is dead")

    def is_alive(self) -> bool:
        """
        Checks if the car is still active.

        Returns:
            bool: True if the car is alive, False otherwise.
        """
        return self.alive
    
    def reset_position(self):
        """
        Resets the car's position, velocity, and angle to default values.
        """
        self.x = 150
        self.y = 150
        self.vel = 0
        self.angle = 0

"""
mannualCar: Represents a manually controlled car that inherits from the Car class.
This car is controlled by keyboard inputs.
"""
class mannualCar(Car):
    def __init__(self):
        """
            Initializes a mannualCar instance with predefined attributes for image, velocity, and position.
            Attributes:
                img (pygame.Surface): The image representing the car.
                max_vel (int): The maximum velocity of the car.
                rotation_vel (int): The rotational velocity of the car.
                x (int): The initial x-coordinate of the car's position.
                y (int): The initial y-coordinate of the car's position.
        """
        super().__init__(RED_CAR, 5, 5, 150, 250)
    
    def mannual_drive(self):
        """
        Enables manual control of the car using keyboard inputs:
        - 'A': Rotate left.
        - 'D': Rotate right.
        - 'W': Move forward.
        - 'S': Move backward.
        If no movement keys are pressed, the car decelerates gradually.
        """
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

    
"""
    autonomousCar: Represents an AI-driven car that inherits from the Car class.
    This car uses radar sensors to detect its surroundings and navigate autonomously.
"""
class autonomousCar(Car):
    def __init__(self):
        """
        Initializes an autonomousCar instance with predefined attributes for image, velocity, position,
        and radar configuration.

         Attributes:
            img (pygame.Surface): The image representing the car.
            max_vel (int): The maximum velocity of the car.
            rotation_vel (int): The rotational velocity of the car.
            x (int): The initial x-coordinate of the car's position.
            y (int): The initial y-coordinate of the car's position.
            radar_angles (list[int]): The angles of the car's radar sensors relative to its orientation.
            radars (list[tuple]): Stores radar data as (angle, distance) tuples.
        """
        super().__init__(GREEN_CAR, 5, 5, 140, 250)
        self.radar_angles = [30, 60, 90, 120, 150]
        self.radars=[]

    def autonomous_drive(self):
        """
        Executes autonomous driving logic:
        - Clears radar data.
        - Moves the car forward and rotates as needed.
        - Draws radar sensors to detect obstacles.
        - Checks for collisions and updates radar data for AI input.
        """
        self.radars.clear()
        self.move_foward()
        self.rotate()
        self.draw_radar(WINDOW, TRACK_BORDER_MASK)
        self.check_collision(TRACK_BORDER_MASK)
        self.get_radar_data()

    def draw_radar(self, window: pygame.Surface, mask: pygame.mask):
        """
        Draws radar sensors to detect obstacles and calculates the distance to the nearest object
        for each radar angle.

        Args:
            window (pygame.Surface): The game window where radar visuals are drawn.
            mask (pygame.Mask): The mask of the surface to be detected by the radar, help prevent collision in advance.
        """
        # for each radar sensor, increment its range until either reaches max length or detect an obstacle
        for ray_angle in self.radar_angles:
            max_length = self.img.get_width()*7
            length = 0
            center_x, center_y = self.get_center_position()
            while length <= max_length:
                radar_x = int(center_x + length * math.cos(math.radians(self.angle + ray_angle)))
                radar_y = int(center_y - length * math.sin(math.radians(self.angle + ray_angle)))
                if mask.get_at((radar_x, radar_y)):
                    break
                length += 1
            
            # Draw the radar visuals
            pygame.draw.line(window, (255, 255, 255), (center_x, center_y), (radar_x, radar_y), 1)
            pygame.draw.circle(window, (0,255,0), (radar_x, radar_y), 3)

            # Calculate distance between the center of the car and the tip of the radar's ray
            dist = int(math.sqrt((radar_x - center_x)**2 + (radar_y - center_y)**2))

             # Store radar data as (angle, distance)
            self.radars.append((ray_angle, dist))

    def get_radar_data(self) -> list:
        """
        Retrieves radar data as a list of distances, representing the inputs for an AI agent.

        Returns:
            list[int]: A list of distances for each radar sensor.
        """
        inputs = [0, 0, 0, 0, 0]
        for i, radar in enumerate(self.radars):
            inputs[i] = int(radar[1])
        return inputs