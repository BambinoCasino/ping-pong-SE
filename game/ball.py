import pygame
import random

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height, paddle_sound, wall_sound, score_sound):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Initial velocity
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])

        # Sound effects
        self.paddle_sound = paddle_sound
        self.wall_sound = wall_sound
        self.score_sound = score_sound

    def move(self, player, ai):
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Bounce off top/bottom walls
        if self.y <= 0:
            self.y = 0
            self.velocity_y *= -1
            self.wall_sound.play()
        elif self.y + self.height >= self.screen_height:
            self.y = self.screen_height - self.height
            self.velocity_y *= -1
            self.wall_sound.play()

        # Paddle collision
        for paddle in (player, ai):
            if self.rect().colliderect(paddle.rect()):
                self.velocity_x *= -1

                # Move ball outside the paddle
                if self.velocity_x > 0:
                    self.x = paddle.x + paddle.width
                else:
                    self.x = paddle.x - self.width

                # Adjust Y velocity based on hit position
                offset = (self.y + self.height / 2) - (paddle.y + paddle.height / 2)
                self.velocity_y = offset * 0.15
                self.paddle_sound.play()
                break

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])
        self.score_sound.play()

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
