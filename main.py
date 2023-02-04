import random

import pygame

from game.history import save_history, get_max_points
from game.models import Background, FlyBird, DownBird, Obstacle

pygame.init()

W = 1280
H = 631
FPS = 60
speed = 2.5
points = 0
is_show = 0

cur_res_font = pygame.font.Font(None, 70)
total_res_font = pygame.font.Font(None, 60)
hint_font = pygame.font.Font(None, 50)

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
    obstacle1.reduce_size(1.7)

    obstacle2 = Obstacle([W + 30, 0 + noise])
    obstacle2.reduce_size(1.7)

    return obstacle1, obstacle2


obstacles.append(add_obstacle())

ground = H - bird.image.get_height() // 2
jump_force = 8
move = jump_force + 1


gamestart = False
is_jumped = False
is_loose = False


while True:
    is_show += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not gamestart and not is_loose:
                gamestart = True
                pygame.time.set_timer(pygame.USEREVENT, 2000)
            if event.key == pygame.K_SPACE and gamestart:
                bird = FlyBird([bird.rect.centerx, bird.rect.centery])
                move = -jump_force
                is_jumped = True
        if event.type == pygame.USEREVENT and gamestart and not is_loose:
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
            points += 1
            obstacles.pop(0)

    for obst1, obst2 in obstacles:
        sc.blit(obst1.image, obst1.rect)
        sc.blit(obst2.image, obst2.rect)
    if gamestart:
        tmp_points = 0
        for obst1, obst2 in obstacles:
            if obst1.rect.colliderect(bird.rect) or obst2.rect.colliderect(bird.rect):
                gamestart = False
                is_loose = True
                points += tmp_points

                cur_res = cur_res_font.render(f"Результат: {points}", True, (0, 0, 0))
                res_rect = cur_res.get_rect()
                res_rect.center = (W // 2, H // 2)
                sc.blit(cur_res, res_rect)

                save_history(point=points)
                break

            tmp_points += 1
    if is_loose:
        cur_res = cur_res_font.render(f"Результат: {points}", True, (0, 0, 0))
        res_rect = cur_res.get_rect()
        res_rect.center = (W // 2, H // 2)
        sc.blit(cur_res, res_rect)
    elif not gamestart:
        total_res = total_res_font.render(
            f"Рекорд: {get_max_points()}", True, (0, 0, 0)
        )
        total_res_rect = total_res.get_rect()
        total_res_rect.x = 20
        total_res_rect.y = 20
        sc.blit(total_res, total_res_rect)

        if is_show >= 0:
            hint = hint_font.render(
                f"Чтобы продолжить игру, нажмите на пробел", True, (50, 50, 50)
            )
            hint_rect = total_res.get_rect()
            hint_rect.center = (W // 2 - 250, H // 2 - 200)
            sc.blit(hint, hint_rect)
            if is_show == 30:
                is_show = -30

    sc.blit(bird.image, bird.rect)
    pygame.display.update()
    clock.tick(FPS)
