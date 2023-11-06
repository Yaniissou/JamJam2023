import pygame
import os

# Initialisation de Pygame
pygame.init()

# Paramètres
FPS = 15
largeur_fenetre = 1024
hauteur_fenetre = 768

# Création de la fenêtre
fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre))
pygame.display.set_caption("Animation de personnage")

# Chargement des images
dossier_assets = "assets/player"
dossier_assets2 = "assets/blanchon"
images_personnage = [pygame.image.load(os.path.join(dossier_assets, f"Player{i}.png")) for i in range(0, 5)]
images_blanchon = [pygame.image.load(os.path.join(dossier_assets2, f"blanchon{i}.png")) for i in range(0, 2)]

# Réglage de la vitesse de l'animation
horloge = pygame.time.Clock()

# Variables pour la gestion des déplacements
deplacement_x = 0
deplacement_y = 0

# Position initiale des personnages
pos_x_personnage = 100
pos_y_personnage = 100
pos_x_blanchon = 300
pos_y_blanchon = 100

# Boucle principale
terminer = False
index_image_personnage = 0
index_image_blanchon = 0
en_deplacement = False

while not terminer:
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            terminer = True
        elif evenement.type == pygame.KEYDOWN:
            if evenement.key == pygame.K_UP:
                deplacement_y = -5
                en_deplacement = True
            elif evenement.key == pygame.K_DOWN:
                deplacement_y = 5
                en_deplacement = True
            elif evenement.key == pygame.K_LEFT:
                deplacement_x = -5
                en_deplacement = True
            elif evenement.key == pygame.K_RIGHT:
                deplacement_x = 5
                en_deplacement = True
        elif evenement.type == pygame.KEYUP:
            if evenement.key == pygame.K_UP:
                deplacement_y = 0
            elif evenement.key == pygame.K_DOWN:
                deplacement_y = 0
            elif evenement.key == pygame.K_LEFT:
                deplacement_x = 0
            elif evenement.key == pygame.K_RIGHT:
                deplacement_x = 0
            en_deplacement = False

    # Mettre à jour la position des personnages
    pos_x_personnage += deplacement_x
    pos_y_personnage += deplacement_y

    # Afficher l'animation ou l'image par défaut pour le personnage
    fenetre.fill((0, 0, 0))  # Effacer la fenêtre
    if en_deplacement:
        fenetre.blit(images_personnage[index_image_personnage], (pos_x_personnage, pos_y_personnage))
        index_image_personnage = (index_image_personnage + 1) % len(images_personnage)
    else:
        fenetre.blit(images_personnage[0], (pos_x_personnage, pos_y_personnage))  # Afficher l'image par défaut

    # Afficher l'animation ou l'image par défaut pour le blanchon
    if en_deplacement:
        fenetre.blit(images_blanchon[index_image_blanchon], (pos_x_blanchon, pos_y_blanchon))
        index_image_blanchon = (index_image_blanchon + 1) % len(images_blanchon)
    else:
        fenetre.blit(images_blanchon[0], (pos_x_blanchon, pos_y_blanchon))  # Afficher l'image par défaut

    pygame.display.flip()

    # Régulation de la vitesse de l'animation
    horloge.tick(FPS)

# Quitter Pygame
pygame.quit()
