import pygame
from pygame.locals import *

class Enemy(pygame.sprite.Sprite):
    
    def __init__(self, x, y, images):
        super().__init__()
        
        # Chargez les images et les screamers
        self.images = images
        
        self.image_index = 0  # Indice de l'image en cours
        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.vitesse = 3
        self.animation_speed = 2  # Vitesse d'animation (plus le nombre est élevé, plus l'animation est lente)
        self.animation_counter = 0
        
        self.direction = 1  # 1 pour avancer, -1 pour reculer
        self.direction_y = 1  # 1 pour descendre, -1 pour monter
        self.collided = False

    def deplacer(self,joueur):
        if not self.rect.colliderect(joueur.rect):
            # Avancer ou reculer en fonction de la direction
            self.rect.x += self.vitesse * self.direction
            self.rect.y += self.vitesse * self.direction_y  # Ajout de cette ligne pour le mouvement vertical
            
            # Inverser la direction s'il atteint un bord de l'écran
            if self.rect.right > 1024 or self.rect.left < 0:
                self.direction = -self.direction
            if self.rect.bottom > 768 or self.rect.top < 0:  # Ajout de cette condition pour le rebond vertical
                self.direction_y = -self.direction_y

            self.animer()

    def animer(self):
        self.animation_speed = 10
        self.animation_counter += 1
        if self.animation_counter >= self.animation_speed:
            self.image_index = (self.image_index + 1) % 2  
            self.image = self.images[self.image_index]
            self.animation_counter = 0

            
    