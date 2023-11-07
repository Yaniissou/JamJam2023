import pygame
import sys

# Initialisation de Pygame
pygame.init()

# Définir les dimensions de la fenêtre
WINDOW_SIZE = (1024, 768)
WINDOW = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Labyrinthe")

# Chargement des images
player_image = pygame.image.load("assets/player/boy/Player1.png")
player_image = pygame.transform.scale(player_image, (40, 40))


class Wall:
    def __init__(self, row, col):
        self.rect = pygame.Rect(col * 40, row * 40, 40, 40)

class Player:
    def __init__(self, row, col):
        self.rect = pygame.Rect(col * 40, row * 40, 40, 40)

# Définir la fonction iterate pour parcourir les caractères dans une ligne
def iterate(line):
    for column_number, block in enumerate(line):
        yield column_number, block

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

# Créer un joueur
player = Player(1, 1)

# Boucle principale du jeu
clock = pygame.time.Clock()
while True:
    clock.tick(30)
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

    # Effacer l'écran
    WINDOW.fill((255, 255, 255))

    # Dessiner les murs
    for wall in level:
        pygame.draw.rect(WINDOW, (0, 0, 0), wall.rect)

    # Dessiner le joueur
    WINDOW.blit(player_image, player.rect.topleft)

    # Mettre à jour l'affichage
    pygame.display.flip()
