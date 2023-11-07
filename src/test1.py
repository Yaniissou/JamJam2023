import pygame
from pygame.locals import *
from gamestate import GameState
from button import Button
from player import Player

#inits
pygame.init()
pygame.font.init()
pygame.mixer.init()

clock = pygame.time.Clock()

#define dimensions
window_width = 1024
window_height = 768

joueur = Player(512,334,1)
window = pygame.display.set_mode((window_width, window_height))

run = True
while run:
    clock.tick(60)
    window.fill((0,0,0))
    window.blit(joueur.image,joueur.rect)
    joueur.deplacer()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
      
        
    pygame.display.update()
pygame.quit()
    