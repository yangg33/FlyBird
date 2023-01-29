import random

import pygame

from game.models import Background, FlyBird, DownBird, Obstacle

pygame.init()

W = 1280
H = 631
FPS = 60
speed = 2.5

sc = pygame.display.set_mode((W, H))
pygame.display.set_caption("Fly Bird")
pygame.display.set_icon(pygame.image.load("images/icon.ico"))

clock = pygame.time.Clock()
background = Background("images/background.jpg", [0, 0])
sc.blit(background.image, background.rect)

bird = FlyBird([W // 2, H // 2])
sc.blit(bird.image, bird.rect)

obstacles = []


def add_obstacle():
    global obstacles
    noise = random.randint(-100, 100)
    obstacle1 = Obstacle([W + 30, H + noise])
    obstacle1.reduce_size(1.6)

    obstacle2 = Obstacle([W + 30, 0 + noise])
    obstacle2.reduce_size(1.6)

    return obstacle1, obstacle2


obstacles.append(add_obstacle())

ground = H - bird.image.get_height() // 2
jump_force = 8
move = jump_force + 1
gamestart = False
is_jumped = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not gamestart:
                gamestart = True
                pygame.time.set_timer(pygame.USEREVENT, 2000)
            if event.key == pygame.K_SPACE and gamestart:
                bird = FlyBird([bird.rect.centerx, bird.rect.centery])
                move = -jump_force
                is_jumped = True
        if event.type == pygame.USEREVENT:
            obstacles.append(add_obstacle())
    if move <= 0:
        bird = DownBird([bird.rect.centerx, bird.rect.centery])
    else:
        bird = FlyBird([bird.rect.centerx, bird.rect.centery])

    if is_jumped:
        if 0 <= bird.rect.centery + move < ground:
            bird.rect.centery += move
            move += 1
        elif bird.rect.centery + move < 0:
            bird.rect.centery = 0
            move += 1
        else:
            bird.rect.centery = ground
            move = jump_force + 1
            is_jumped = False

    sc.blit(background.image, background.rect)

    if gamestart:
        for obst1, obst2 in obstacles:
            obst1.rect.centerx -= speed
            obst2.rect.centerx -= speed

            sc.blit(obst1.image, obst1.rect)
            sc.blit(obst2.image, obst2.rect)
        while len(obstacles) != 0 and obstacles[0][0].rect.centerx < -30:
            obstacles.pop(0)

    sc.blit(bird.image, bird.rect)
    pygame.display.update()
    clock.tick(FPS)
