import pygame 
class CleUSB:
    def __init__(self, x, y):
        self.image = pygame.image.load("assets/elements/usbkey.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def check_collision(self, joueur):
        return self.rect.colliderect(joueur.rect) 