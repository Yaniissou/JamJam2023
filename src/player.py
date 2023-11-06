import pygame

class Player(pygame.sprite.Sprite) :
    def __init__(self,x,y,) :
        super().__init__()
        self.image = pygame.Surface((50, 50))  
        self.image.fill((0, 255, 0))  

        self.rect = self.image.get_rect()  
        self.rect.center = (x, y)  

        self.vitesse = 10
        
    def deplacer(self) :
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= self.vitesse
        if keys[pygame.K_RIGHT]:
            self.x += self.vitesse
        if keys[pygame.K_UP]:
            self.y -= self.vitesse
        if keys[pygame.K_DOWN]:
            self.y += self.vitesse