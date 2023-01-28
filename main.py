import pygame

from game.models import Background, Bird, FlyBird, DownBird

pygame.init()

W = 1280
H = 631
FPS = 60

sc = pygame.display.set_mode((W, H))
pygame.display.set_caption("Fly Bird")
pygame.display.set_icon(pygame.image.load("images/icon.ico"))

clock = pygame.time.Clock()
background = Background("images/background.jpg", [0, 0])
sc.blit(background.image, background.rect)

bird = FlyBird([W//2, H//2])
sc.blit(bird.image, bird.rect)

ground = H - bird.image.get_height() // 2
jump_force = 15
move = jump_force + 1
gamestart = False
is_jumped = False
while True:
    for event in pygame.event.get():
        if event.type== pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not gamestart:
                gamestart = True
            elif event.key == pygame.K_SPACE and gamestart:
                move = -jump_force
                is_jumped = True
    if move <= 0:
        bird = DownBird([bird.rect.centerx, bird.rect.centery])
    else:
        bird = FlyBird([bird.rect.centerx, bird.rect.centery])

    if is_jumped:
        if 0 <=  bird.rect.centery + move < ground:
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
    sc.blit(bird.image, bird.rect)
    pygame.display.update()
    clock.tick(FPS)
