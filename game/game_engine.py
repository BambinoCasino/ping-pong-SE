import pygame
from .paddle import Paddle
from .ball import Ball

WHITE = (255, 255, 255)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.SysFont("Arial", 30)

        self.winning_score = 5  # default
        self.game_over = False

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def update(self, screen):
        if not self.game_over:
            # Move the ball and handle collisions
            self.ball.move(self.player, self.ai)

            # Check for scoring
            if self.ball.x <= 0:
                self.ai_score += 1
                self.ball.reset()
            elif self.ball.x >= self.width:
                self.player_score += 1
                self.ball.reset()

            # AI paddle tracking with difficulty based on winning score
            difficulty_map = {3: 0.9, 5: 1.0, 7: 1.2}
            difficulty = difficulty_map.get(self.winning_score, 1.0)
            self.ai.auto_track(self.ball, self.height, difficulty)

            # Check for game over
            self.check_game_over(screen)
        else:
            # Display replay menu
            self.replay_menu(screen)

    def render(self, screen):
        # Draw paddles and ball
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width // 2, 0), (self.width // 2, self.height))

        # Draw score
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width // 4, 20))
        screen.blit(ai_text, (self.width * 3 // 4, 20))

    def check_game_over(self, screen):
        winner_text = ""
        if self.player_score >= self.winning_score:
            winner_text = "Player Wins!"
        elif self.ai_score >= self.winning_score:
            winner_text = "AI Wins!"

        if winner_text:
            self.game_over = True
            screen.fill((0, 0, 0))
            text_surface = self.font.render(winner_text, True, WHITE)
            text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2))
            screen.blit(text_surface, text_rect)
            pygame.display.flip()
            pygame.time.delay(1000)  # brief pause before replay menu

    def replay_menu(self, screen):
        screen.fill((0, 0, 0))
        menu_texts = [
            "Play Again - Choose Winning Score:",
            "3: Best of 3",
            "5: Best of 5",
            "7: Best of 7",
            "ESC: Exit"
        ]

        for i, line in enumerate(menu_texts):
            text_surface = self.font.render(line, True, WHITE)
            text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2 - 60 + i*40))
            screen.blit(text_surface, text_rect)

        pygame.display.flip()

        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_3:
                        self.winning_score = 3
                        waiting_for_input = False
                    elif event.key == pygame.K_5:
                        self.winning_score = 5
                        waiting_for_input = False
                    elif event.key == pygame.K_7:
                        self.winning_score = 7
                        waiting_for_input = False
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()

        # Reset game state for replay
        self.player_score = 0
        self.ai_score = 0
        self.ball.reset()
        self.game_over = False
