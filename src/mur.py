import pygame

class Mur:
    def __init__(self, x, y):
        self.image = pygame.image.load("assets/elements/beacon.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)