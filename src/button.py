import pygame

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
    def draw(self, screen):
		#draw button
        screen.blit(self.image, (self.rect.x, self.rect.y))
        
    def isClicked(self):
        action = False
        
		#get mouse position
        pos = pygame.mouse.get_pos()
        

		#check if mouse is over the button
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                print("Start button clicked")
                action = True 
                return action   
   