import pygame

from game.constans import W, H
from game.handler import Game
from game.models import Background, FlyBird

pygame.init()


sc = pygame.display.set_mode((W, H))
pygame.display.set_caption("Fly Bird")
pygame.display.set_icon(pygame.image.load("images/icon.ico"))

background = Background("images/background.jpg", [0, 0])

game = Game()
game.start_game(sc, background)
game.events_handler()
