import pygame

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
    def draw(self, screen):
		#dessine le bouton à l'ecran
        screen.blit(self.image, (self.rect.x, self.rect.y))
        
    def isClicked(self):
        action = False
        
		#recupere la position de la souris
        pos = pygame.mouse.get_pos()
        

		#verifie si la souris survole le bouton
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                print("Start button clicked")
                action = True 
                return action   
            
            
    def isHovered(self):
        action = False
        pos = pygame.mouse.get_pos()
        
        if self.rect.collidepoint(pos):
            action = True
        return action      
    
    def setImage(self, image):
        self.image = image
   