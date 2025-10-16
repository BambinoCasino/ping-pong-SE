import pygame
from game.game_engine import GameEngine

# Initialize pygame and mixer
pygame.init()
pygame.mixer.init()  # Enables sound playback

# Screen dimensions
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong - Pygame Version")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Create game engine
engine = GameEngine(WIDTH, HEIGHT)

def main():
    running = True
    while running:
        SCREEN.fill(BLACK)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Input, update, render
        engine.handle_input()
        engine.update(SCREEN)  # pass SCREEN for drawing and replay menu
        engine.render(SCREEN)

        # Refresh display
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
