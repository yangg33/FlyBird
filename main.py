import pygame

from game.models import Background, Bird

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
bird = Bird('images/bird.png', [W//2, H//2])
bird.reduce_size(2)
sc.blit(bird.image, bird.rect)

while True:
    for event in pygame.event.get():
        if event.type== pygame.QUIT:
            exit()
        
    pygame.display.update()
    clock.tick(FPS)
