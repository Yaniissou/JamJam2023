import pygame
from pygame.locals import *
from gamestate import GameState
from button import Button
from player import Player
from enemy import Enemy
import random #pour generer la position x et y des objets de manière aléatoire
from usb import CleUSB
from mur import Mur,WallLaby
import time #pour gerer le rythme


pygame.init()
screen_width = 1024
screen_height = 768
WINDOW_SIZE = (screen_width, screen_height)
window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Labyrinthe")
level = []
clock = pygame.time.Clock()
image_bg = pygame.image.load("assets/bg/bg.png")
joueur = Player(100,100,1)
cle_usb = CleUSB(920, 650)
gagne = False
perdu = False
font = pygame.font.Font("fonts/Minecraft.ttf", 72)
images = [
        pygame.image.load("assets/blanchon/Blanchon00.png"),
        pygame.image.load("assets/blanchon/Blanchon11.png")
        ]
enemyLaby = Enemy(500,500,images)
lampe = pygame.image.load('assets/elements/circleTest.png')
gameMusic = pygame.mixer.Sound("assets/sounds/musics/game_theme.ogg")
BPM = 124 #battements par seconde de la musique du jeu
BEAT_INTERVAL = 60 / BPM  # Intervalle entre les battements par secondes 
BEAT_TOLERANCE = 0.08  # Tolerance de mauvais timing
key_pressed = False
last_beat_time = pygame.time.get_ticks() / 1000 - BEAT_INTERVAL
error_count = 0 #nombre d'erreurs de timing autorisé

def iterate(line):
    for column_number, block in enumerate(line):
        yield column_number, block
        
def genererLabyLevel():
    global level
    with open("assets/labyrinthe/level.txt") as level_file:
        line_file = level_file.readline()
        line_number = 0
        while line_file:
            for column_number, block in iterate(line_file):
                if block == "+":
                    level.append(WallLaby(line_number, column_number))
            line_file = level_file.readline()
            line_number += 1
            
def playingModLabyrinthe(window):
    global gagne
    global font
    global key_pressed
    global error_count
    global last_beat_time
    global perdu
    global start_time
    gameMusic.play()
    window.fill((255,255,255))
    joueur.deplacer()   
    if event.type == pygame.KEYDOWN and not key_pressed and not gagne:
                key_pressed = True
                start_time = time.time()  # Enregistre le temps auquel la touche a été enfoncée
                if (event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):
                    #print("je suis dans la boucle1")
                    current_time = time.time()
                    if current_time - last_beat_time >= BEAT_INTERVAL - BEAT_TOLERANCE and current_time - last_beat_time <= BEAT_INTERVAL + BEAT_TOLERANCE and error_count < 2:
                        #print("je suis dans la boucle2")
                        print("Bon timing")
                        joueur.deplacer()       
                        if cle_usb.check_collision(joueur):
                            print("Partie gagnée")
                            gagne = True        
                            #return GameState.VICTORY
                    else:
                        error_count += 1
                        print("Mauvais timing")
  
                    if error_count >= 2:
                        font = pygame.font.Font("fonts/Minecraft.ttf", 72)
                        texte = font.render("Partie perdu !", True, (0, 0, 0))
                        window.blit(texte, (330 , 420))
                        joueur.arreter_animation()
                        #return GameState.LOSER
                        
                    last_beat_time = current_time
    elif event.type == pygame.KEYUP:
        key_pressed = False
        start_time = None
    
    
    for wall in level:
        if joueur.rect.colliderect(wall.rect):
            overlap_x = joueur.rect.width / 2 + wall.rect.width / 2 - abs(joueur.rect.centerx - wall.rect.centerx)
            overlap_y = joueur.rect.height / 2 + wall.rect.height / 2 - abs(joueur.rect.centery - wall.rect.centery)

            if overlap_x < overlap_y:
                if joueur.rect.centerx < wall.rect.centerx:
                    joueur.rect.right = wall.rect.left
                else:
                    joueur.rect.left = wall.rect.right
            else:
                if joueur.rect.centery < wall.rect.centery:
                    joueur.rect.bottom = wall.rect.top
                else:
                    joueur.rect.top = wall.rect.bottom
    window.blit(image_bg, (0, 0))
    for wall in level:
        pygame.draw.rect(window, (0, 0, 0), wall.rect)
    window.blit(joueur.image, joueur.rect.topleft)
    
   
        
        
    
    
    window.blit(cle_usb.image, cle_usb.rect)    
    if gagne:
        font = pygame.font.Font("fonts/Minecraft.ttf", 72)
        texte = font.render("Partie gagnee !", True, (0, 0, 0))
        
        window.blit(texte, (330 , 420))
            
        joueur.arreter_animation()
    else: #code pour activer/desactiver la lampe torche
        filter = pygame.surface.Surface((1024, 768))
        filter.fill(pygame.color.Color('White'))
        filter.blit(lampe, (joueur.rect.centerx-200, joueur.rect.centery-200))
        window.blit(filter, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)    
genererLabyLevel()        
run = True
while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    playingModLabyrinthe(window)
      
    pygame.display.update()
        
pygame.quit()
        