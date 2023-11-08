import pygame
import time

# Initialisation de Pygame
pygame.init()

# Paramètres
FRAMERATE = 60
BPM = 124
BEAT_INTERVAL = 60 / BPM  # Intervalle entre les battements en secondes (ex: 0.5 pour 120 BPM)
BEAT_TOLERANCE = 0.06  # Tolerance pour les clics en secondes

# Initialisation de la fenêtre
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Jeu de Rythme")

# Chargement de la musique
pygame.mixer.music.load("assets/sounds/musics/game_theme.ogg")

# Fonction pour clignoter en rouge
def flash_red():
    screen.fill((255, 0, 0))
    pygame.display.flip()
    time.sleep(0.1)  # Durée du clignotement en secondes
    screen.fill((255, 255, 255))  # Retour à l'écran blanc
    pygame.display.flip()

# Fonction principale
def main():
    clock = pygame.time.Clock()
    pygame.mixer.music.play()
    last_beat_time = pygame.time.get_ticks() / 1000 - BEAT_INTERVAL
    error_count = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):
                print("Espace appuyé")
                current_time = time.time()
                if current_time - last_beat_time >= BEAT_INTERVAL - BEAT_TOLERANCE and current_time - last_beat_time <= BEAT_INTERVAL + BEAT_TOLERANCE:
                    flash_red()
                else:
                    error_count += 1

                if error_count >= 2:
                    print("Trop d'erreurs, la musique s'arrête.")
                    running = False

                last_beat_time = current_time

        pygame.display.flip()
        clock.tick(FRAMERATE)

    pygame.quit()


if __name__ == "__main__":
    main()
