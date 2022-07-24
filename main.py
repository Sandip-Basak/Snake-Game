import pygame
import random
import math
import time
from pygame import mixer

pygame.init()

# Game Window
window = pygame.display.set_mode((1000, 800))
pygame.display.set_caption("Snake")
game_icon = pygame.image.load("snake.png")
pygame.display.set_icon(game_icon)
clock = pygame.time.Clock()

# Background Audio
mixer.music.load("background music.mp3")
mixer.music.play(-1)

# Snake
snake_length = 1
snake = pygame.image.load("square.png").convert()
snake_x = []
snake_y = []
for j in range(snake_length):
    snake_x.append(32)
    snake_y.append(32)
snake_move = 32
move = "right"

# Food
mouse = pygame.image.load("mouse.png")
mouse_x = random.randint(50, 750)
mouse_y = random.randint(50, 550)

# Score
score = 0

# Text
game_over = pygame.font.Font('04B_19.TTF', 64)
score_text = pygame.font.Font('04B_19.TTF', 25)
restart_text = pygame.font.Font('04B_19.TTF', 25)

# Game Condition
game = "play"


def is_collision(x1, y1, x2, y2):
    distance = math.sqrt((math.pow(x1 - x2, 2)) + (math.pow(y1 - y2, 2)))
    if distance < 25:
        return True
    else:
        return False


def score_display():
    score_blit = score_text.render("Score : " + str(score), True, (0, 0, 0))
    window.blit(score_blit, (865, 20))


def mouse_display(x, y):
    window.blit(mouse, (x, y))


def snake_display():
    for k in range(snake_length):
        window.blit(snake, (snake_x[k], snake_y[k]))


def eating(x1, y1, x2, y2):
    distance = math.sqrt((math.pow(x1 - x2, 2)) + (math.pow(y1 - y2, 2)))
    if distance < 25:
        return True
    else:
        return False


def ending_window():
    over = game_over.render("GAME OVER", True, (0, 0, 0))
    restart_blit = restart_text.render("PRESS ENTER TO RESTART", True, (0, 0, 0))
    window.blit(over, (345, 300))
    window.blit(restart_blit, (367, 400))


# Credits
window.fill((0, 0, 0))
info_name = game_over.render("SNAKE GAME", True, (225, 225, 225))
created_by = score_text.render("CREATED BY", True, (225, 225, 225))
creator = score_text.render("SANDIP", True, (225, 225, 225))
window.blit(info_name, (300, 300))
window.blit(created_by, (430, 400))
window.blit(creator, (450, 450))
pygame.display.update()
time.sleep(1.25)

# Game loop
loop = True
while loop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if move == "down" or game == "pause":
                    break
                move = "up"
            if event.key == pygame.K_RIGHT:
                if move == "left" or game == "pause":
                    break
                move = "right"
            if event.key == pygame.K_DOWN:
                if move == "up" or game == "pause":
                    break
                move = "down"
            if event.key == pygame.K_LEFT:
                if move == "right" or game == "pause":
                    break
                move = "left"
            if event.key == pygame.K_RETURN:
                if game == "play":
                    break
                score = 0
                snake_x[0] = 32
                snake_y[0] = 32
                game = "play"
                move = "right"
                mouse_x = random.randint(50, 750)
                mouse_y = random.randint(50, 550)

    # Display
    window.fill((85, 205, 81))
    score_display()

    # Snake Movement
    for i in range(snake_length - 1, 0, -1):
        snake_x[i] = snake_x[i - 1]
        snake_y[i] = snake_y[i - 1]

    if move == "up":
        snake_y[0] -= snake_move
    elif move == "down":
        snake_y[0] += snake_move
    elif move == "right":
        snake_x[0] += snake_move
    elif move == "left":
        snake_x[0] -= snake_move
    snake_display()

    # Mouse position
    mouse_display(mouse_x, mouse_y)

    # Eating Check
    if eating(mouse_x, mouse_y, snake_x[0], snake_y[0]):
        ding = mixer.Sound('ding.mp3')
        ding.play()
        score += 1
        snake_length += 1
        snake_x.append(-1)
        snake_y.append(-1)
        mouse_x = random.randint(50, 750)
        mouse_y = random.randint(50, 550)

    # Collision Check
    for i in range(3, snake_length):
        if is_collision(snake_x[i], snake_y[i], snake_x[0], snake_y[0]):
            # Crash Audio
            crash = mixer.Sound('crash.mp3')
            crash.play()

            snake_x[0] = 1500
            snake_y[0] = 1500
            snake_length = 1
            game = "pause"
            mouse_x = 2000
            mouse_y = 2000
    # Boundary Check
    if game == "play":
        if snake_x[0] > 990 or snake_x[0] < 10 or snake_y[0] > 775 or snake_y[0] < 10:
            border_crash = mixer.Sound('crash.mp3')
            border_crash.play()
            snake_x[0] = 1500
            snake_y[0] = 1500
            snake_length = 1
            game = "pause"
            mouse_x = 2000
            mouse_y = 2000

    # Gaming End
    if game == "pause":
        ending_window()

    pygame.display.update()
    clock.tick(12)
