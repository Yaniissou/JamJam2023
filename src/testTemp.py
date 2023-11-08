import pygame
from pygame.locals import *
from gamestate import GameState
from button import Button
from player import Player
from enemy import Enemy

pygame.init()
clock = pygame.time.Clock()
window = pygame.display.set_mode((1024, 768))
images = [
    pygame.image.load("assets/blanchon/Blanchon0.png"),
    pygame.image.load("assets/blanchon/Blanchon1.png")
]

images_scream = [
    pygame.image.load("assets/blanchon/screamer/Blanchon0.png"),
    pygame.image.load("assets/blanchon/screamer/Blanchon1.png"),
    pygame.image.load("assets/blanchon/screamer/Blanchon2.png")
]
enemy = Enemy(800, 334, images)
joueur = Player(50, 50, 0)
animation_counter = 0
image_scream_index = 0  # Initialisez l'indice de l'animation de screamer
pygame.mixer.music.load("assets/sounds/game_over/darwin.mp3")
def animer_screamer(images_screams):
    global animation_counter
    global image_scream_index
    animation_speed = 2
    animation_counter += 1
    if animation_counter >= animation_speed:
        image_scream_index = (image_scream_index + 1) % len(images_screams)
        enemy.image = images_screams[image_scream_index]
        animation_counter = 0


# Définissez quelques variables pour le clignotement de l'arrière-plan
run = True
screamer_start_time = 0  # Initialisez le temps de début de l'animation du screamer

while run:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if enemy.rect.colliderect(joueur.rect):
        
        if screamer_start_time == 0:
            # En cas de collision, réinitialisez les positions des personnages en haut à gauche
            joueur.rect.topleft = (0, 0)
            enemy.rect.topleft = (0, 0)

            # Commencez l'animation du screamer
            screamer_start_time = pygame.time.get_ticks()  # Enregistrez le moment où l'animation du screamer commence
            pygame.mixer.music.play()
        
        # Appel de la fonction pour animer le Screamer
        

        # Obtenez le temps écoulé depuis le début de l'animation
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - screamer_start_time

        # Alternez les couleurs de fond entre noir et rouge pendant l'animation du screamer
        if elapsed_time % 250 < 125:
            background_color = (0, 0, 0)
        else:
            background_color = (255, 0, 0)

        window.fill(background_color)
        window.blit(images_scream[0], (150, 30))
        animer_screamer(images_scream)
        pygame.display.update()

        if elapsed_time > 2000:  # Arrêtez l'effet après 2 secondes (ajustez le temps si nécessaire)
            run = False
    else:
        enemy.deplacer(joueur)
        window.fill((0, 0, 0))
        window.blit(enemy.image, enemy.rect)
        joueur.deplacer()
        window.blit(joueur.image, joueur.rect)
        pygame.display.update()

pygame.quit()
