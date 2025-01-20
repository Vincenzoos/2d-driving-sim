import neat
import os
from world import eval_genomes

# setup NEAT neural network
def run(config_path):
    """
    Sets up and runs the NEAT neural network simulation.

    Args:
        config_path (str): The file path to the NEAT configuration file.

    Workflow:
        1. Loads the NEAT configuration.
        2. Initializes a NEAT population based on the configuration.
        3. Attaches reporters for logging and statistics.
        4. Executes the NEAT algorithm, using `eval_genomes` as the evaluation function for 50 generations at most.
    """
    global pop
     # Load NEAT configuration from the specified file
    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )

    # Initialize NEAT population
    pop = neat.Population(config)

    # Attach reporters for monitoring the simulation process
    # Console output for generation progress
    pop.add_reporter(neat.StdOutReporter(True))
    # Collects statistics for visualization and analysis
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)

    # Run the fitness function for 50 generations
    pop.run(eval_genomes, 50)

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    run(config_path)