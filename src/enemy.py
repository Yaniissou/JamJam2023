import pygame
from pygame.locals import *

class Enemy(pygame.sprite.Sprite):
    
    def __init__(self, x, y,images):
        super().__init__()
        
        # Chargez les images et les screamers
        self.images = images
        
        
        self.image_index = 0  # Indice de l'image en cours
        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.vitesse = 5
        self.animation_speed = 2  # Vitesse d'animation (plus le nombre est élevé, plus l'animation est lente)
        self.animation_counter = 0
        
        self.direction = 1  # 1 pour avancer, -1 pour reculer
        self.collided = False

    def deplacer(self,joueur):
        if not self.collided:
            # Avancer ou reculer en fonction de la direction
            self.rect.x += self.vitesse * self.direction
            self.animer()
            # Inverser la direction s'il atteint un bord de l'écran
            if self.rect.right > 1024:
                self.direction = -1
            elif self.rect.left < 0:
                self.direction = 1
            
            
        elif self.rect.colliderect(joueur.rect):
            print("en collision")
            # Lorsqu'il y a une collision, jouer l'animation de screamers
            self.animer_screamers()

        
    def animer(self):
        self.animation_speed = 10
        self.animation_counter += 1
        if self.animation_counter >= self.animation_speed:
            self.image_index = (self.image_index + 1) % 2  
            self.image = self.images[self.image_index]
            self.animation_counter = 0
            
    
    def animer_screamers(self):
        self.animation_speed = 10
        self.animation_counter += 1
        if self.animation_counter >= self.animation_speed:
            self.image_index = (self.image_index + 1) % len(self.images)  # Boucler les images d'animation
            self.image = self.images[self.image_index]
            self.animation_counter = 0
