import pygame
from world import eval_genomes, run_mannual
from asset import *
import neat
import os

# Constants for the menu
MENU_WIDTH, MENU_HEIGHT = 800, 600
MENU_BG_COLOR = (0, 0, 0)
TEXT_COLOR = (255, 255, 255)
FONT = pygame.font.Font(None, 50)

# Game configuration
pygame.display.set_caption("Driving Simulator - Menu")
clock = pygame.time.Clock()
FPS = 60

def draw_menu():
    """
    Draws the main menu with two options: Manual Mode and AI Mode.
    """
    WINDOW.fill(MENU_BG_COLOR)

    # Title
    title_text = FONT.render("Driving Simulator", True, TEXT_COLOR)
    title_rect = title_text.get_rect(center=(MENU_WIDTH // 2, MENU_HEIGHT // 4))
    WINDOW.blit(title_text, title_rect)

    # Manual mode option
    manual_text = FONT.render("1. Manual Mode", True, TEXT_COLOR)
    manual_rect = manual_text.get_rect(center=(MENU_WIDTH // 2, MENU_HEIGHT // 2))
    WINDOW.blit(manual_text, manual_rect)

    # AI mode option
    ai_text = FONT.render("2. AI Mode", True, TEXT_COLOR)
    ai_rect = ai_text.get_rect(center=(MENU_WIDTH // 2, MENU_HEIGHT // 1.5))
    WINDOW.blit(ai_text, ai_rect)

    # Update the display
    pygame.display.update()

def menu_loop():
    """
    Displays the main menu and waits for the user to select an option.
    
    Returns:
        str: The mode selected by the user ("manual" or "ai").
    """
    while True:
        draw_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "manual"
                elif event.key == pygame.K_2:
                    return "ai"
        clock.tick(FPS)

def run_simulation(mode: str):
    """
    Starts the game loop based on the selected mode.

    Args:
        mode (str): The selected mode ("manual" or "ai").
    """
    if mode == "manual":
        run_mannual()

    elif mode == "ai":
        # Run the game with AI simulation
        local_dir = os.path.dirname(__file__)
        config_path = os.path.join(local_dir, 'config.txt')
        run_neat(config_path)

def run_neat(config_path):
    """
    Configures and runs the NEAT simulation.
    
    Args:
        config_path (str): Path to the NEAT configuration file.
    """
    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )
    pop = neat.Population(config)

    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)

    pop.run(eval_genomes, 150)

if __name__ == "__main__":
    selected_mode = menu_loop()
    run_simulation(selected_mode)
