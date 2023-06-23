import time

import pygame
from pygame.locals import *

# Constants
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700
BRICK_WIDTH = 60
BRICK_HEIGHT = 20
PADDLE_WIDTH = 80
PADDLE_HEIGHT = 12
BALL_RADIUS = 10
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
PINK = (255, 192, 203)
LIGHT_PINK = (255, 192, 193)
HOT_PINK = (255, 105, 180)
DEEP_PINK = (255, 20, 147)
LIGHT_CYAN = (224, 255, 255)
DARK_CYAN = (0, 139, 139)
LIGHT_CYAN = (224, 255, 255)
AQUAMARINE = (127, 255, 212)
DARK_BLUE = (0, 0, 139)
MEDIUM_BLUE = (0, 0, 205)
BLUE = (0, 0, 255)
ROYAL_BLUE = (65, 105, 225)
BEISH=(245,245,220)


class Brick:
    def __init__(self, x, y, points, color):
        self.rect = pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT)
        self.alive = True
        self.points = points
        self.color = color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

class Paddle:
    def __init__(self):
        self.rect = pygame.Rect(
            SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2,
            SCREEN_HEIGHT  - PADDLE_HEIGHT - 10,
            PADDLE_WIDTH,
            PADDLE_HEIGHT,
        )
        self.speed = 50

    def move(self, direction):
        if direction == "left":
            self.rect.x -= self.speed
        elif direction == "right":
            self.rect.x += self.speed

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

    def draw(self, surface):
        pygame.draw.rect(surface, RED, self.rect)

class Ball:
    def __init__(self):
        self.rect = pygame.Rect(SCREEN_WIDTH // 2 - BALL_RADIUS, SCREEN_HEIGHT // 2 - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)
        self.velocity = [4, 4]
        self.brick_sound = pygame.mixer.Sound("C:\\Users\\asus\\Downloads\\mixkit-funny-break-engine-2944.wav")  # Path to sound effect file

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.velocity[0] = -self.velocity[0]

        if self.rect.top <= 0:
            self.velocity[1] = -self.velocity[1]

    def draw(self, surface):
        pygame.draw.circle(surface, DEEP_PINK, self.rect.center, BALL_RADIUS)

    def play_brick_sound(self):
        self.brick_sound.play()

class Scoreboard:
    def __init__(self):
        self.score = 0
        self.font = pygame.font.Font(None, 36)
        self.box_rect = pygame.Rect(10, 10, 150, 50)  # Position and size of the scoreboard box

    def increase_score(self, points):
        self.score += points

    def decrease_score(self, points):
        self.score -= points

    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, self.box_rect, 2)  # Draw the scoreboard box

        score_text = self.font.render("Score: " + str(self.score), True, WHITE)
        text_rect = score_text.get_rect()
        text_rect.center = self.box_rect.center  # Center the score text within the box

        surface.blit(score_text, text_rect)

class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Brick Break")

        self.bricks = []
        self.create_bricks()

        self.paddle = Paddle()
        self.ball = Ball()
        self.scoreboard = Scoreboard()

        self.game_over = False

    def create_bricks(self):
        points = 1  # Starting points for the first brick
        colors = [DARK_BLUE, MEDIUM_BLUE, BLUE, ROYAL_BLUE]  # Colors for different rows
        for row in range(4):
            for column in range(10):
                x = column * (BRICK_WIDTH + 5) + 30
                y = row * (BRICK_HEIGHT + 5) + 30
                brick = Brick(x, y, points, colors[row])
                self.bricks.append(brick)
            points += 1  # Increase points for each subsequent row


        color=[GREEN,RED,BLACK]
        for row in range(1):
            pts=1
            for column in range(10):
                x = column * (BRICK_WIDTH + 5) + 30
                y = SCREEN_HEIGHT -(row * (BRICK_HEIGHT + 5) + 30)
                #y = SCREEN_HEIGHT - BRICK_HEIGHT - 30
                brick = Brick(x, y, pts, color[row] )  # Negative points for the bottom bricks
                self.bricks.append(brick)
            pts += 1
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()
            elif event.type == KEYDOWN:
                if event.key == K_LEFT:
                    self.paddle.move("left")
                elif event.key == K_RIGHT:
                    self.paddle.move("right")

    def update(self):
        if self.game_over:
            return

        self.ball.update()

        if self.ball.rect.colliderect(self.paddle.rect):
            self.ball.velocity[1] = -self.ball.velocity[1]

        for brick in self.bricks:
            if brick.alive and self.ball.rect.colliderect(brick.rect):
                self.ball.velocity[1] = -self.ball.velocity[1]
                brick.alive = False
                if brick.points > 0:
                    self.scoreboard.increase_score(brick.points)
                else:
                    self.scoreboard.decrease_score(abs(brick.points))
                self.ball.play_brick_sound()

        if self.ball.rect.top >= SCREEN_HEIGHT:
            self.end_game()

    def draw(self):
        self.screen.fill(BEISH)
        self.paddle.draw(self.screen)
        self.ball.draw(self.screen)

        for brick in self.bricks:
            if brick.alive:
                brick.draw(self.screen)

        self.scoreboard.draw(self.screen)

        if self.game_over:
            self.draw_game_over()

        pygame.display.flip()

    def draw_game_over(self):
        font = pygame.font.Font(None, 48)
        text = font.render("Game Over", True, BLACK)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(text, text_rect)




    def end_game(self):
        self.game_over = True


    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

            if self.game_over:
                time.sleep(1)
                pygame.quit()
                break
def game1():
    game = Game()
    game.run()
