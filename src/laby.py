#mode labyrinthe inachevée

import pygame
import sys

# Initialisation de Pygame
pygame.init()

# Définir les dimensions de la fenêtre
screen_width = 1024
screen_height = 768
WINDOW_SIZE = (screen_width, screen_height)
WINDOW = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Labyrinthe")

# Chargement des images
player_image = pygame.image.load("assets/player/boy/Player1.png")
player_image = pygame.transform.scale(player_image, (40, 40))
lampe = pygame.image.load('assets/elements/circle.png')
image_usbkey = pygame.image.load("assets/elements/usbkey.png")
image_bureau = pygame.image.load("assets/elements/bureau2.png")


class Wall:
    def __init__(self, row, col):
        self.rect = pygame.Rect(col * 32, row * 32, 32, 32)

class Player:
    def __init__(self, row, col):
        self.rect = pygame.Rect(col * 40, row * 40, 40, 40)

# Définir la fonction iterate pour parcourir les caractères dans une ligne
def iterate(line):
    for column_number, block in enumerate(line):
        yield column_number, block
        
class CleUSB:
    def __init__(self, x, y):
        self.image = image_usbkey
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def check_collision(self, joueur):
        return self.rect.colliderect(joueur.rect)
    
class Bureau:
    def __init__(self, x, y):
        self.image = image_bureau
        self.rect = self.image.get_rect()
        self.rect.center = (x , y)
        self.rect.width = 64
        self.rect.height = 48
        
        
    def check_collision(self, joueur):
        
        return self.rect.colliderect(joueur.rect)         

# Chargement du niveau à partir du fichier texte
level = []
with open("assets/labyrinthe/level.txt") as level_file:
    line_file = level_file.readline()
    line_number = 0
    while line_file:
        for column_number, block in iterate(line_file):
            if block == "+":
                level.append(Wall(line_number, column_number))
        line_file = level_file.readline()
        line_number += 1

# Création des sprites
player = Player(1, 1)
cle_usb = CleUSB(screen_width / 2 - 25, screen_height / 2 + 25)
bureau = Bureau(screen_width / 2 , screen_height / 2  )

gagne = False

clock = pygame.time.Clock()
while True:
    clock.tick(15)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Gérer les mouvements du joueur
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        player.rect.move_ip(0, -40)
    if keys[pygame.K_DOWN]:
        player.rect.move_ip(0, 40)
    if keys[pygame.K_LEFT]:
        player.rect.move_ip(-40, 0)
    if keys[pygame.K_RIGHT]:
        player.rect.move_ip(40, 0)
        
   
        
    if cle_usb.check_collision(player):
        print("Partie gagnée")
        gagne = True
        
        

    # Vérifier les collisions avec les murs
    for wall in level:
        if player.rect.colliderect(wall.rect):
            # Si une collision est détectée, annuler le mouvement
            if keys[pygame.K_UP]:
                player.rect.move_ip(0, 40)
            if keys[pygame.K_DOWN]:
                player.rect.move_ip(0, -40)
            if keys[pygame.K_LEFT]:
                player.rect.move_ip(40, 0)
            if keys[pygame.K_RIGHT]:
                player.rect.move_ip(-40, 0)
                
    if bureau.check_collision(player):
        # Si une collision est détectée, annuler le mouvement
        if keys[pygame.K_UP]:
            player.rect.move_ip(0, 40)
        if keys[pygame.K_DOWN]:
            player.rect.move_ip(0, -40)
        if keys[pygame.K_LEFT]:
            player.rect.move_ip(40, 0)
        if keys[pygame.K_RIGHT]:
            player.rect.move_ip(-40, 0)            

    
    WINDOW.fill((255, 255, 255))

    # Dessiner les murs
    for wall in level:
        pygame.draw.rect(WINDOW, (0, 0, 0), wall.rect)

    # Dessiner le joueur
    WINDOW.blit(player_image, player.rect.topleft)
    
    
    
    WINDOW.blit(bureau.image, bureau.rect)
    
    WINDOW.blit(cle_usb.image, cle_usb.rect)
    
    #allume la lampe torche
    """if gagne == False:
        filter = pygame.surface.Surface((screen_width, screen_height))
        filter.fill(pygame.color.Color('White'))
        filter.blit(lampe, (player.rect.centerx-100, player.rect.centery-100))
        WINDOW.blit(filter, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)"""

    # Mettre à jour l'affichage
    pygame.display.flip()
