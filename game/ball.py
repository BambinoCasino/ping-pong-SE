import pygame
import random

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Random initial velocity
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])

    def move(self, player, ai):
        # Move the ball
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Bounce off top and bottom walls
        if self.y <= 0:
            self.y = 0
            self.velocity_y *= -1
        elif self.y + self.height >= self.screen_height:
            self.y = self.screen_height - self.height
            self.velocity_y *= -1

        # Check collision with paddles
        for paddle in (player, ai):
            if self.rect().colliderect(paddle.rect()):
                # Reverse X velocity
                self.velocity_x *= -1

                # Move ball just outside the paddle to prevent sticking
                if self.velocity_x > 0:
                    self.x = paddle.x + paddle.width
                else:
                    self.x = paddle.x - self.width

                # Adjust Y velocity based on where the ball hits the paddle
                offset = (self.y + self.height/2) - (paddle.y + paddle.height/2)
                self.velocity_y = offset * 0.15  # tweak multiplier for responsiveness
                break

    def reset(self):
        # Reset ball to center
        self.x = self.original_x
        self.y = self.original_y

        # Randomize direction
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
