import pygame
from pygame.locals import *


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y,gender):
        super().__init__()
        
        
        self.gender = gender
        if gender ==0:                      #0 si garcon et 1 si fille
            self.images = [
                pygame.image.load("assets/player/Player00.png"),  # Image d'idle
                pygame.image.load("assets/player/Player11.png"),  # Image d'idle
                pygame.image.load("assets/player/Player22.png"),  # Walk cycle
                pygame.image.load("assets/player/Player33.png"),  # Walk cycle
                pygame.image.load("assets/player/Player44.png"),  # Walk cycle
                pygame.image.load("assets/player/Player55.png")   # Walk cycle
        ]
        elif gender == 1:
             self.images = [
                pygame.image.load("assets/playerFemale/PlayerFemal0.png"),  # Image d'idle
                pygame.image.load("assets/playerFemale/PlayerFemal1.png"),  # Image d'idle
                pygame.image.load("assets/playerFemale/PlayerFemal2.png"),  # Walk cycle
                pygame.image.load("assets/playerFemale/PlayerFemal3.png"),  # Walk cycle
                pygame.image.load("assets/playerFemale/PlayerFemal4.png"),  # Walk cycle
                pygame.image.load("assets/playerFemale/PlayerFemal5.png")   # Walk cycle
            ]   
            # Ajoutez les autres images d'animation
        self.image_index = 0  # Indice de l'image en cours
        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.vitesse = 3
        self.animation_speed = 2  # Vitesse d'animation (plus le nombre est élevé, plus l'animation est lente)
        self.animation_counter = 0  # Compteur pour gérer l'animation

    
    def deplacer(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.vitesse
            self.animer()
        elif keys[pygame.K_RIGHT]:
            self.rect.x += self.vitesse
            self.animer()
        elif keys[pygame.K_UP]:
            self.rect.y -= self.vitesse
            self.animer()
        elif keys[pygame.K_DOWN]:
            self.rect.y += self.vitesse
            self.animer()
        else:
        # Si le joueur ne se déplace pas, afficher l'animation d'idle
           self.animer_idle()

    def animer_idle(self):
    # Gérer l'animation d'idle en changeant d'image à la vitesse définie
        self.animation_speed = 10
        self.animation_counter += 1
        if self.animation_counter >= self.animation_speed:
            self.image_index = (self.image_index + 1) % 2  # Boucler entre les deux premières images
            self.image = self.images[self.image_index]
            self.animation_counter = 0
        
    def animer(self):
        # Gérer l'animation en changeant d'image à la vitesse définie
        self.animation_speed = 2
        self.animation_counter += 1
        if self.animation_counter >= self.animation_speed:
            self.image_index = (self.image_index + 1) % len(self.images)  # Boucler les images d'animation
            self.image = self.images[self.image_index]
            self.animation_counter = 0
    
    def arreter_animation(self):
        
       
        self.image = self.images[0]  # Image d'idle du garçon
        self.image_index = 0
        self.animation_counter = 0
        self.vitesse = 0       
