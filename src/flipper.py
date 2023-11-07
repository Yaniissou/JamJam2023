import pygame
import sys
import random

# Initialisation de Pygame
pygame.init()

# Définir la taille de la fenêtre
screen_width = 1024
screen_height = 768
fenetre = pygame.display.set_mode((screen_width, screen_height))

# Charger les images

image_mur = pygame.image.load("assets/elements/beacon.png")
image_joueur = pygame.image.load("assets/player/boy/Player1.png")
image_usbkey = pygame.image.load("assets/elements/usbkey.png")
image_bg = pygame.image.load("assets/bg/bg.png")
lampe = pygame.image.load('assets/elements/circle.png')

# Créer une classe pour le joueur
class Joueur:
    def __init__(self, x, y):
        self.image = image_joueur
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.vitesse = 5

    def deplacer(self, dx, dy):
        new_x = self.rect.x + dx
        new_y = self.rect.y + dy

        if 0 <= new_x <= screen_width - self.rect.width and 0 <= new_y <= screen_height - self.rect.height:
            self.rect.x = new_x
            self.rect.y = new_y

# Créer une classe pour les murs
class Mur:
    def __init__(self, x, y):
        self.image = image_mur
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

# Créer une classe pour la cléUSB        
class CleUSB:
    def __init__(self, x, y):
        self.image = image_usbkey
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def check_collision(self, joueur):
        return self.rect.colliderect(joueur.rect) 

# Générer les murs
murs = []
nb_murs = 60
for _ in range(nb_murs):  # Changer le nombre de murs si besoin
    x = random.randint(0, screen_width - image_mur.get_width())
    y = random.randint(0, screen_height - image_mur.get_height())
    
    # Vérifier la distance avec les murs existants
    collision = False
    for mur in murs:
        distance_x = abs(mur.rect.x - x)
        distance_y = abs(mur.rect.y - y)
        if distance_x < 32 or distance_y < 32:
            collision = True
            break
    
    if not collision:
        murs.append(Mur(x, y))

# Générer la clé USB
cle_usb = CleUSB(0, 0)

while True:
    x = random.randint(0, screen_width - image_usbkey.get_width())
    y = random.randint(0, screen_height - image_usbkey.get_height())
    cle_usb.rect.topleft = (x, y)

    # Vérifier la distance avec les murs
    collision = False
    for mur in murs:
        distance_x = abs(mur.rect.x - x)
        distance_y = abs(mur.rect.y - y)
        if distance_x < 32 or distance_y < 32:
            collision = True
            break
    
    if not collision:
        break

# Créer un objet joueur
joueur = Joueur(50, 50)

# Boucle principale du jeu
clock = pygame.time.Clock()


while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    touches = pygame.key.get_pressed()
    dx = (touches[pygame.K_RIGHT] - touches[pygame.K_LEFT]) * joueur.vitesse
    dy = (touches[pygame.K_DOWN] - touches[pygame.K_UP]) * joueur.vitesse

    joueur.deplacer(dx, dy)
    
    if cle_usb.check_collision(joueur):
        print("Partie gagnée")

    for mur in murs:
        if joueur.rect.colliderect(mur.rect):
            print("Collision avec le mur")

            overlap_x = joueur.rect.width - abs(joueur.rect.centerx - mur.rect.centerx)
            overlap_y = joueur.rect.height - abs(joueur.rect.centery - mur.rect.centery)

            if overlap_x < overlap_y:
                if dx > 0:
                    joueur.rect.right = mur.rect.left
                else:
                    joueur.rect.left = mur.rect.right
            else:
                if dy > 0:
                    joueur.rect.bottom = mur.rect.top
                else:
                    joueur.rect.top = mur.rect.bottom

    fenetre.blit(image_bg, (0, 0))
    fenetre.blit(cle_usb.image, cle_usb.rect)

    for mur in murs:
        fenetre.blit(mur.image, mur.rect)
    fenetre.blit(joueur.image, joueur.rect)
    
    # Ajouter le code pour la lampe torche ici
    filter = pygame.surface.Surface((screen_width, screen_height))
    filter.fill(pygame.color.Color('White'))
    filter.blit(lampe, (joueur.rect.centerx-100, joueur.rect.centery-100))
    fenetre.blit(filter, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)

    pygame.display.flip()