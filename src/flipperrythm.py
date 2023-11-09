import pygame
import sys
import random
import time

# Initialisation de Pygame
pygame.init()

# Définir la taille de la fenêtre
screen_width = 1024
screen_height = 768
fenetre = pygame.display.set_mode((screen_width, screen_height))

# Charger les images

image_mur = pygame.image.load("assets/elements/beacon.png")
image_joueur = pygame.image.load("assets/player/Player11.png")
image_usbkey = pygame.image.load("assets/elements/usbkey.png")
image_bg = pygame.image.load("assets/bg/bg.png")
lampe = pygame.image.load('assets/elements/circleTEST.png')

# Paramètres gerant le rythme
BPM = 124 #battements par seconde de la musique du jeu
BEAT_INTERVAL = 60 / BPM  # Intervalle entre les battements par secondes 
BEAT_TOLERANCE = 0.06  # Tolerance de mauvais timing
key_pressed = False

# Créer une classe pour le joueur
class Joueur:
    def __init__(self, x, y):
        self.image = image_joueur
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.vitesse = 30

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
    
    # Vérifier la distance avec les murs existants, pour ne pas les superposer
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
last_beat_time = pygame.time.get_ticks() / 1000 - BEAT_INTERVAL
error_count = 0
gagne = False


#chargement de la musique du jeu
pygame.mixer.music.load("assets/sounds/musics/game_theme.ogg")
pygame.mixer.music.play()

def loser():
    font = pygame.font.Font("fonts/Minecraft.ttf", 72)
    texte = font.render("Partie perdue !", True, (0, 0, 0))
    fenetre.blit(texte, (800 // 2 - texte.get_width() // 2, 600 // 2 - texte.get_height() // 2))
    pygame.mixer.music.stop()
    

while True:
      
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.KEYDOWN and not key_pressed and not gagne:
                key_pressed = True
                start_time = time.time()  # Enregistrez le temps auquel la touche a été enfoncée
                if (event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):
                    
                    current_time = time.time()
                    if current_time - last_beat_time >= BEAT_INTERVAL - BEAT_TOLERANCE and current_time - last_beat_time <= BEAT_INTERVAL + BEAT_TOLERANCE and error_count < 2:
                        print("Bon timing")
                        old_rect_position = joueur.rect.copy()
                        touches = pygame.key.get_pressed()
                        dx = (touches[pygame.K_RIGHT] - touches[pygame.K_LEFT]) * joueur.vitesse
                        dy = (touches[pygame.K_DOWN] - touches[pygame.K_UP]) * joueur.vitesse
                        joueur.deplacer(dx, dy)
                        
                        for mur in murs:
                            if joueur.rect.colliderect(mur.rect):
                                joueur.rect = old_rect_position
                                
                        if cle_usb.check_collision(joueur):
                            print("Partie gagnée")
                            gagne = True        
                    else:
                        error_count += 1
                        print("Mauvais timing")
  
                    if error_count >= 2:
                        loser()

                    last_beat_time = current_time
        elif event.type == pygame.KEYUP:
                key_pressed = False
                start_time = None
                
        fenetre.blit(image_bg, (0, 0))
        fenetre.blit(cle_usb.image, cle_usb.rect)
        
        for mur in murs:
            fenetre.blit(mur.image, mur.rect)
        fenetre.blit(joueur.image, joueur.rect)
        
        if gagne:
            font = pygame.font.Font("fonts/Minecraft.ttf", 72)
            texte = font.render("Partie gagnee !", True, (0, 0, 0))
            fenetre.blit(texte, (screen_width // 2 - texte.get_width() // 2, screen_height // 2 - texte.get_height() // 2))
            pygame.mixer.music.stop()
        else:
            filter = pygame.surface.Surface((screen_width, screen_height))
            filter.fill(pygame.color.Color('White'))
            filter.blit(lampe, (joueur.rect.centerx-200, joueur.rect.centery-200))
            fenetre.blit(filter, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)              

        # Vérifie si le joueur a maintenu la touche pendant plus d'une seconde
    if key_pressed and start_time is not None and time.time() - start_time >= 1:
            loser()
            key_pressed = False    

    pygame.display.flip()
    clock.tick(60)