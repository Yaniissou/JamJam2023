import pygame
import time

# Initialisation de Pygame
pygame.init()

# Paramètres gerant le rythme
FRAMERATE = 60
BPM = 124 #battements par seconde de la musique du jeu
BEAT_INTERVAL = 60 / BPM  # Intervalle entre les battements par secondes 
BEAT_TOLERANCE = 0.06  # Tolerance de mauvais timing
key_pressed = False

# Initialisation de la fenêtre
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Jeu de Rythme")

# Chargement de la musique
pygame.mixer.music.load("assets/sounds/musics/game_theme.ogg")

def flash_red():
    screen.fill((255, 0, 0))
    pygame.display.flip()
    time.sleep(0.1)  # Durée du clignotement en secondes
    screen.fill((255, 255, 255))  # Retour à l'écran blanc
    pygame.display.flip()

def loser():
    font = pygame.font.Font("fonts/Minecraft.ttf", 72)
    texte = font.render("Partie perdue !", True, (0, 0, 0))
    screen.blit(texte, (800 // 2 - texte.get_width() // 2, 600 // 2 - texte.get_height() // 2))
    pygame.mixer.music.stop()
    
clock = pygame.time.Clock()
pygame.mixer.music.play()
last_beat_time = pygame.time.get_ticks() / 1000 - BEAT_INTERVAL
error_count = 0

running = True
while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and not key_pressed:
                key_pressed = True
                start_time = time.time()  # Enregistrez le temps auquel la touche a été enfoncée
                if (event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):
                    
                    current_time = time.time()
                    if current_time - last_beat_time >= BEAT_INTERVAL - BEAT_TOLERANCE and current_time - last_beat_time <= BEAT_INTERVAL + BEAT_TOLERANCE:
                        flash_red()
                        print("Bon timing")
                    else:
                        error_count += 1
                        print("Mauvais timing")

                    if error_count >= 2:
                        loser()

                    last_beat_time = current_time
            elif event.type == pygame.KEYUP:
                key_pressed = False
                start_time = None  

        # Vérifie si le joueur a maintenu la touche pendant plus d'une seconde
        if key_pressed and start_time is not None and time.time() - start_time >= 1:
            loser()
            key_pressed = False  

        pygame.display.flip()
        clock.tick(FRAMERATE)
        
pygame.quit()




