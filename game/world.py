import pygame
from car import mannualCar, autonomousCar
import neat
from asset import *


pygame.init()

# Game config
FPS = 60
clock = pygame.time.Clock()
game_objects = [(GRASS, (0,0)), (TRACK, (0,0)), (FINISH_LINE, FINISH_LINE_POSITION), (TRACK_BORDER, (0,0))]
player_car = mannualCar()
ai_car = autonomousCar()


def draw_objects(window: pygame.Surface, objects):
    for obj, pos in objects:
        window.blit(obj, pos)
    # car.draw(window)
    # Update the game each iteration
    pygame.display.update()

def eliminate(index):
    cars.pop(index)
    ge.pop(index)
    neural_nets.pop(index)

# def eval_genomes():
def eval_genomes(genomes, config):
    # Game loop
    run = True
    global cars, ge, neural_nets
    cars = []
    ge = []
    neural_nets = []
    THRESHOLD = 0.7

    # for each generation, update cars, genome and neural nets lists
    for genome_id, genome in genomes:
        cars.append(autonomousCar())
        ge.append(genome)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        neural_nets.append(net)

        # Set initial fitness of each car in each generation to zero
        genome.fitness = 0

    while run:
        # Limit clock to 60 fps, ensure all machine run the game on the same speed
        clock.tick(FPS)
        draw_objects(WINDOW, game_objects)

        # Event check
        for event in pygame.event.get():
            # Stop the game if game window exit button was clicked
            if event.type == pygame.QUIT:
                run = False
                break

        # Stop the game if all cars in one generation are destroyed
        if len(cars) == 0:
            break

        # Update fitness point of each car, enliminate it from the game
        for i, car in enumerate(cars):
            ge[i].fitness += 1
            if not car.is_alive():
                eliminate(i)

        # Activate Steering action in autopilot mode for each car
        for i, car in enumerate(cars):
            output = neural_nets[i].activate(car.get_radar_data())
            if output[0] > THRESHOLD:
                car.rotate(left=True)
            if output[1] > THRESHOLD:
                car.rotate(right=True)
            if output[0] <= THRESHOLD and output[1] <= THRESHOLD:
                car.rotate()

        # Update the state of car in autopilot mode for each car
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
        pygame.display.update()

    # Game termination
    # pygame.quit()
