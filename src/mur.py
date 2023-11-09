import pygame

class Mur:
    def __init__(self, x, y):
        self.image = pygame.image.load("assets/elements/beacon.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        
class WallLaby:
    def __init__(self, row, col):
        self.rect = pygame.Rect(col * 32, row * 32, 32, 32)       
        