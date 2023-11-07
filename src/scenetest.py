import pygame
from pygame.locals import *
from player import Player
import sys
from button import Button

# Initialisation de Pygame
pygame.init()
pygame.font.init()

# Définir la taille de la fenêtre

font = pygame.font.Font("fonts/Minecraft.ttf", 36)
fontsprite = pygame.font.Font("fonts/Minecraft.ttf", 26)
window_width = 1024
window_height = 768

window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Choix du sprite')
pygame.mixer.music.load("assets/sounds/musics/starting.ogg")

GREY = (105, 105, 105)
text = font.render("Faites votre choix", False, (255, 255, 255))
text_rect = text.get_rect()
text_rect.center = (window_width/2, window_height/4 -100)
btnSprite1 = Button(window_width/2-215, window_height/1.25+40, pygame.image.load("assets/buttons/btnsprite.png"))
btnSprite2 = Button(window_width/2+190, window_height/1.25+40, pygame.image.load("assets/buttons/btnsprite.png"))

textsprite1 = fontsprite.render("Sprite 1", False, (255, 255, 255))
textsprite1_rect = textsprite1.get_rect()
textsprite1_rect.center = (window_width/2-210, window_height/1.25+10)

textsprite2 = fontsprite.render("Sprite 2", False, (255, 255, 255))
textsprite2_rect = textsprite1.get_rect()
textsprite2_rect.center = (window_width/2+195, window_height/1.25+10)

imagesprite1 = pygame.image.load("assets/player/Player0.png")
imagesprite2 = pygame.image.load("assets/blanchon/Blanchon0.png")

surface1 = pygame.Surface((200, 300))
surface1.fill((150, 150, 150))

surface2 = pygame.Surface((200, 300))
surface2.fill((150, 150, 150))
window.fill(GREY)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # L'utilisateur a appuyé sur la touche "Espace"
                pygame.mixer.music.play()  # Jouez la musique que vous avez chargée
                # Ici, vous pouvez ajouter la logique pour passer à une autre partie du jeu ou du menu

    window.fill(GREY)
    window.blit(text, text_rect)
    
    
    window.blit(surface1, (window_width // 4-50, window_height // 2-100))
    window.blit(surface2, (window_width // 2+100, window_height // 2-100))
    window.blit(imagesprite1,(window_width // 4-180, window_height // 2-200))
    window.blit(imagesprite2,(window_width // 2-50,  window_height // 2-200))
    btnSprite1.draw(window)
    btnSprite2.draw(window)
    window.blit(textsprite1, textsprite1_rect)
    window.blit(textsprite2, textsprite2_rect)
    pygame.display.update()
    pygame.display.flip()

pygame.quit()
sys.exit()

pygame.display.update()
pygame.display.flip()