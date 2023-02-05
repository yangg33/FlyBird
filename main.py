import pygame

from game.constans import W, H
from game.handler import Game
from game.models import Background, FlyBird
from misc.converter_path import resource_path

pygame.init()


sc = pygame.display.set_mode((W, H))
pygame.display.set_caption("Fly Bird")
pygame.display.set_icon(pygame.image.load(resource_path("images/icon.ico")))

background = Background(resource_path("images/background.jpg"), [0, 0])

game = Game()
game.start_game(sc, background)
game.events_handler()
