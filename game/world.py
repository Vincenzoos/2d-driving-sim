import pygame
from car import mannualCar, autonomousCar
import neat
from asset import *

# Game environment intialization
pygame.init()

# Game Configuration
# Frames per second for the game loop
FPS = 60
# Clock to control the game loop speed
clock = pygame.time.Clock()
# List of game objects and their positions
game_objects = [
    (GRASS, (0,0)), 
    (TRACK, (0,0)), 
    (FINISH_LINE, (110, 200)), 
    (TRACK_BORDER, (0,0))
]
# Human-controlled car
player_car = mannualCar()
# AI-controlled car
ai_car = autonomousCar()


def draw_objects(window: pygame.Surface, objects: list):
    """
    Draws all game objects onto the window.

    Args:
        window (pygame.Surface): The surface representing the game window.
        objects (list[tuple[pygame.Surface, tuple[int, int]]]): A list of objects to draw, 
            where each object is a tuple containing a surface and its position on the screen.
    """
    for obj, pos in objects:
        window.blit(obj, pos)
    # car.draw(window)
    # Update the game each iteration
    pygame.display.update()


def eliminate(index: int):
    """
    Eliminates a car, its corresponding genome, and its neural network from the simulation.

    Args:
        index (int): The index of the car to eliminate.
    """
    cars.pop(index)
    ge.pop(index)
    neural_nets.pop(index)


def eval_genomes(genomes: list, config: neat.Config):
    """
    Evaluates each genome in a NEAT population by simulating autonomous driving.

    Args:
        genomes (list[tuple[int, neat.Genome]]): A list of genomes to evaluate.
        config (neat.Config): The NEAT configuration object.
    """
    # Initialize global variables for cars, genomes, and neural networks
    global cars, ge, neural_nets
     # List of AI-controlled cars
    cars = []
    # List of genomes corresponding to each car
    ge = []
    # List of neural networks for each genome
    neural_nets = []
    # Activation threshold for AI steering decisions
    THRESHOLD = 0.7

    # Create cars, genomes, and neural networks for the current generation
    for genome_id, genome in genomes:
        cars.append(autonomousCar())
        ge.append(genome)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        neural_nets.append(net)

        # Set initial fitness of each genome to zero
        genome.fitness = 0

    # Flag for the main simulation loop
    run = True
    while run:
        # Limit the game loop to the specified FPS
        clock.tick(FPS)
        draw_objects(WINDOW, game_objects)

        # Event handling for quitting the game
        for event in pygame.event.get():
            # Stop the game if game window exit button was clicked
            if event.type == pygame.QUIT:
                run = False
                break

        # Exit loop if all cars are eliminated
        if len(cars) == 0:
            break

        # Update fitness and eliminate cars that are no longer alive
        for i, car in enumerate(cars):
            ge[i].fitness += 1
            if not car.is_alive():
                eliminate(i)

        # AI decision-making for each car
        for i, car in enumerate(cars):
            output = neural_nets[i].activate(car.get_radar_data())
            if output[0] > THRESHOLD:
                car.rotate(left=True)
            if output[1] > THRESHOLD:
                car.rotate(right=True)
            if output[0] <= THRESHOLD and output[1] <= THRESHOLD:
                car.rotate()

        # Update and render each car
        for car in cars:
            car.draw()
            car.autonomous_drive()
        


        # Detect human control via key pressed
        # player_car.mannual_drive() 

        # check for collision
        # if player_car.check_collision(TRACK_BORDER_MASK):
        #     player_car.bounce()
        #     player_car.update_car_status(False)
        
        # finish_line_poi = player_car.check_collision_point(FINISH_LINE_MASK, *FINISH_LINE_POSITION)
        # if finish_line_poi:
        #     if finish_line_poi[1] == 0:
        #         player_car.bounce()
        #     else:
        #         print("You win!")
        #         player_car.reset_position()

        # draw radar
        # player_car.draw_radar(WINDOW, TRACK_BORDER_MASK)

         # Update the game display
        pygame.display.update()

    # Game termination
    # pygame.quit()
