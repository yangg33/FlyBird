import pygame

class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

class Bird(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.location = location
        self.rect.centerx, self.rect.centery = self.location

    def reduce_size (self, to):
        self.image = pygame.transform.scale(self.image, (self.image.get_width() // to, self.image.get_height() //to))
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = self.location

class FlyBird(Bird):
    def __init__(self, location):
        super().__init__("images/fly_bird.png", location)
        self.reduce_size(8)

class DownBird(Bird):
    def __init__(self, location):
        super().__init__("images/down_bird.png", location)
        self.reduce_size(8)