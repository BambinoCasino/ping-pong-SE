import pygame

class Paddle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 7

    def move(self, dy, screen_height):
        self.y += dy
        # Keep paddle within screen
        self.y = max(0, min(self.y, screen_height - self.height))

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def auto_track(self, ball, screen_height, difficulty=1.0):
        """Move paddle automatically to track the ball with adjustable difficulty."""
        adjusted_speed = self.speed * difficulty
        if ball.y < self.y + self.height / 2:
            self.move(-adjusted_speed, screen_height)
        elif ball.y > self.y + self.height / 2:
            self.move(adjusted_speed, screen_height)
