import pygame
from pygame.locals import *
from gamestate import GameState


#vars
gamestate = GameState.START


#inits
pygame.init()
clock = pygame.time.Clock()

pygame.font.init()
font = pygame.font.Font("fonts/Minecraft.ttf", 36)

#define dimensions
window_width = 800
window_height = 600

#create the window
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Save The Exams')

#Create landing text
text = font.render("Save The Exams", False, (0, 0, 0))
text_rect = text.get_rect()
text_rect.center = (400, 100)


#background placeholder
background = pygame.image.load("assets/placeholders/800x600.png")

run = True
while run:
    clock.tick(60)
    
    #draw background
    window.blit(background, (0, 0))
    window.blit(text, text_rect)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    print(gamestate)        
    pygame.display.update()
        
pygame.quit()
            