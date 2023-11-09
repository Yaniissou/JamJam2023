#mode labyrinthe inachevée

import pygame
import sys
from player import Player
from mur import WallLaby
# Initialisation de Pygame
pygame.init()

# Définir les dimensions de la fenêtre
screen_width = 1024
screen_height = 768
WINDOW_SIZE = (screen_width, screen_height)
WINDOW = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Labyrinthe")

# Chargement des images
player_image = pygame.image.load("assets/player/Player00.png")

lampe = pygame.image.load('assets/elements/circle.png')
image_usbkey = pygame.image.load("assets/elements/usbkey.png")
image_bureau = pygame.image.load("assets/elements/bureau3.png")


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
                level.append(WallLaby(line_number, column_number))
        line_file = level_file.readline()
        line_number += 1


# Créer un joueur
joueur = Player(100, 100, 1)



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
    
        
   
    joueur.deplacer()   
    if cle_usb.check_collision(joueur):
        print("Partie gagnée")
        gagne = True
        
        

    # Vérifier les collisions avec les murs
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
        if joueur.rect.colliderect(bureau.rect):
            overlap_x = joueur.rect.width / 2 + bureau.rect.width / 2 - abs(joueur.rect.centerx - bureau.rect.centerx)
            overlap_y = joueur.rect.height / 2 + bureau.rect.height / 2 - abs(joueur.rect.centery - bureau.rect.centery)

            if overlap_x < overlap_y:
                if joueur.rect.centerx < bureau.rect.centerx:
                    joueur.rect.right = bureau.rect.left
                else:
                    joueur.rect.left = bureau.rect.right
            else:
                if joueur.rect.centery < bureau.rect.centery:
                    joueur.rect.bottom = bureau.rect.top
                else:
                    joueur.rect.top = bureau.rect.bottom
    
    WINDOW.fill((255, 255, 255))

    # Dessiner les murs
    for wall in level:
        pygame.draw.rect(WINDOW, (0, 0, 0), wall.rect)

    # Dessiner le joueur
    WINDOW.blit(player_image, joueur.rect.topleft)
    
    
    
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
