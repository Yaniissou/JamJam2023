import pygame
from pygame.locals import *
from gamestate import GameState
from button import Button
from player import Player
from enemy import Enemy

pygame.init()
clock = pygame.time.Clock()
window = pygame.display.set_mode((1024, 768))
images =[
            pygame.image.load("assets/blanchon/Blanchon0.png"),
            pygame.image.load("assets/blanchon/Blanchon1.png"),
            pygame.image.load("assets/blanchon/screamer/screamBlanchon0.png"),
            pygame.image.load("assets/blanchon/screamer/screamBlanchon1.png"),
            pygame.image.load("assets/blanchon/screamer/screamBlanchon2.png")
        ]         
enemy = Enemy(800,334,images)
run = True
while run:
    clock.tick(60)
    window.fill((0,0,0))     
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    enemy.deplacer()        
    window.blit(enemy.image,enemy.rect)
    
    
          
    pygame.display.update()
        
pygame.quit()

