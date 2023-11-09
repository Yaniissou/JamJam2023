import pygame
from pygame.locals import *
from gamestate import GameState
from button import Button
from player import Player
from enemy import Enemy
import random
from usb import CleUSB
from mur import Mur
#inits
pygame.init()
pygame.font.init()
pygame.mixer.init()

clock = pygame.time.Clock()
font = pygame.font.Font("fonts/Minecraft.ttf", 72)
subfont = pygame.font.Font("fonts/Minecraft.ttf", 36)
favicon = pygame.image.load("assets/favicon/favicon.png")
pygame.display.set_icon(favicon)
#element pour labyrinthe
image_bg = pygame.image.load("assets/bg/bg.png")
lampe = pygame.image.load('assets/elements/circleTest.png')
#define dimensions
window_width = 1024
window_height = 768
# Générer les murs
murs = []
nb_murs = 60
for _ in range(nb_murs):  # Changer le nombre de murs si besoin
    x = random.randint(0, 1024 - 32)
    y = random.randint(0, 768 - 32)
    
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
#vars
gamestate = GameState.INITIATING
startButton = Button(window_width/2, window_height/1.25, pygame.image.load("assets/buttons/start.png"))
returnButton = Button(75,window_height - 50, pygame.image.load("assets/buttons/arrow.png"))
gameloop = 0
#bouton pour choisir genre
btnSprite1 = Button(303, 520.4, pygame.image.load("assets/buttons/btnsprite.png"))
btnSprite2 = Button(702, 520.4, pygame.image.load("assets/buttons/btnsprite.png"))
startingtext = font.render("Save The Exams", False, (255, 255, 255))
subtitle =  subfont.render("Infiltrez vous a l'IUT 2 pour sauver vos partiels", False, '#d3d3d3')
iutlogo = pygame.image.load("assets/elements/iut2logo.png")
iutlogo_rect = iutlogo.get_rect()
iutlogo_rect.center = (window_width/2, window_height/2.25)
startingtext_rect = startingtext.get_rect()
startingsubtext_rect = subtitle.get_rect()
startingtext_rect.center = (window_width/2, window_height/4)
startingsubtext_rect.center = (window_width/2, window_height/3)
images = [
        pygame.image.load("assets/blanchon/Blanchon00.png"),
        pygame.image.load("assets/blanchon/Blanchon11.png")
        ]

images_scream = [
        pygame.image.load("assets/blanchon/screamer/Blanchon0.png"),
        pygame.image.load("assets/blanchon/screamer/Blanchon1.png"),
        pygame.image.load("assets/blanchon/screamer/Blanchon2.png")
                ]


ennemies = []
enemy = Enemy(800, 334, images)
enemy2 = Enemy(700, 500, images)
enemy3 = Enemy(600, 200, images)
enemy4 = Enemy(200, 500, images)
enemy5 = Enemy(700, 800, images)
enemy6 = Enemy(300, 500, images)
enemy7 = Enemy(400, 600, images)
enemy8 = Enemy(400, 200, images)
ennemies.append(enemy)
ennemies.append(enemy2)
ennemies.append(enemy3)
ennemies.append(enemy4)
ennemies.append(enemy5)
ennemies.append(enemy6)
ennemies.append(enemy7)
ennemies.append(enemy8)

screamer_start_time = 0
darwinmp3 = pygame.mixer.Sound("assets/sounds/game_over/darwin.mp3")
gameMusic = pygame.mixer.Sound("assets/sounds/musics/game_theme.ogg")
gagne =False
#create the window
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Save The Exams')



#starting background
startingBackground = pygame.image.load("assets/bg/loop.jpg")
#ingame background
ingameBackground = pygame.image.load("assets/bg/bg.png")
start = pygame.mixer.Sound("assets/sounds/musics/starting.ogg")



run = True

"""
METHODES 
"""

def clear(window):
    window.fill((0, 0, 0))

def startGame(window):
    
    print("The game is starting")
    clear(window)   
    window.blit(ingameBackground, (0, 0)) 
    
def initWindow(window,firstRun):
    if(firstRun == False): 
        clear(window)
    else:
        start.play()
    window.blit(startingBackground.subsurface(Rect(0, 0, 1024, 968)), (0, 0))
    window.blit(startingtext, startingtext_rect)
    window.blit(subtitle, startingsubtext_rect)
    window.blit(iutlogo, iutlogo_rect)

    startButton.draw(window)
    start.play()

        
def drawHistory(window):
    infofont = pygame.font.Font("fonts/Minecraft.ttf", 20)
    messages = ["Vous venez de lamentablement foirer vos partiels de mi- semestre,",
                "et la suite semble mal embarquee :/",
                "Votre derniere chance ?",
                "Obtenir 20/20 a tous les examens de la prochaine semaine de partiels !",
                "",
                "Alors que vous aviez abandonne tout espoir, une rumeur commence a se propager dans l'IUT:",
                "",
                "Il existerait une clef USB secrete dans le bureau 101,",
                "regroupant l'integralite des prochains examens...",
                "Votre objectif ?", "Muni d'une lampe torche, vous ",
                "infiltrez l'IUT de nuit pour recuperer la fameuse clef.",
                "Mais attention, des choses etranges se produisent",
                "en dehors des heures d'ouverture..."]
    clear(window)
    window.fill((0, 0, 0))
    historyheight = 120
    for i in range(len(messages)):
        
        historytext = infofont.render(messages[i], False, (255, 255, 255))
        historytext_rect = historytext.get_rect()
        historytext_rect.center = (window_width / 2, historyheight)
        window.blit(historytext, historytext_rect)
        historyheight += 30
        
    returnButton.draw(window)
    startButton.draw(window) 
    
    
screamer_start_time = 0    
def drawCharacter(window) :
    fontsprite = pygame.font.Font("fonts/Minecraft.ttf", 26)


    BLACK = (0, 0, 0)
    text = font.render("Faites votre choix", False, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.center = (window_width/2, window_height/4 -100)
    

    textsprite1 = fontsprite.render("Franck", False, (255, 255, 255))
    textsprite1_rect = textsprite1.get_rect()
    textsprite1_rect.center = (315,490)

    textsprite2 = fontsprite.render("Gaelle", False, (255, 255, 255))
    textsprite2_rect = textsprite1.get_rect()
    textsprite2_rect.center = (720, 490)

    imagesprite1 = pygame.image.load("assets/player/Player1Icon.png")
    imagesprite2 = pygame.image.load("assets/playerFemale/PlayerFemaleIcon.png")

    #surface1 = pygame.Surface((200, 300))
    #surface1.fill((150, 150, 150))

    #surface2 = pygame.Surface((200, 300))
    #surface2.fill((150, 150, 150))
    
    window.fill(BLACK)
    window.blit(startingBackground, (0, 0))
    window.blit(text, text_rect)
    #window.blit(surface1, (window_width // 4-50, window_height // 2-100)) carre gris derriere
    #window.blit(surface2, (window_width // 2+100, window_height // 2-100))
    window.blit(imagesprite1,(76, 184))
    window.blit(imagesprite2,(482,  184))
    btnSprite1.draw(window)
    btnSprite2.draw(window)
    returnButton.draw(window)
    window.blit(textsprite1, textsprite1_rect)
    window.blit(textsprite2, textsprite2_rect)
    
    

def playingMod(window,joueur,gameloop) :
    
    clear(window)  
    start.stop()
    if gameloop == 0:
        gameMusic.play()
    joueur.deplacer()
    global screamer_start_time
    global run
    global gagne
    if cle_usb.check_collision(joueur):
        print("Partie gagnée")
        gagne = True
    for mur in murs:
        if joueur.rect.colliderect(mur.rect):
            overlap_x = joueur.rect.width / 2 + mur.rect.width / 2 - abs(joueur.rect.centerx - mur.rect.centerx)
            overlap_y = joueur.rect.height / 2 + mur.rect.height / 2 - abs(joueur.rect.centery - mur.rect.centery)

            if overlap_x < overlap_y:
                if joueur.rect.centerx < mur.rect.centerx:
                    joueur.rect.right = mur.rect.left
                else:
                    joueur.rect.left = mur.rect.right
            else:
                if joueur.rect.centery < mur.rect.centery:
                    joueur.rect.bottom = mur.rect.top
                else:
                    joueur.rect.top = mur.rect.bottom

    window.blit(image_bg, (0, 0))
    
    for mur in murs:
        window.blit(mur.image, mur.rect)
    window.blit(cle_usb.image, cle_usb.rect)
    # Ajouter le code pour la lampe torche ici
    
    
    for enemy in ennemies:
        if enemy.rect.colliderect(joueur.rect):
        
            if screamer_start_time == 0:
                # En cas de collision, réinitialisez les positions des personnages en haut à gauche
                joueur.rect.topleft = (0, 0)
                enemy.rect.topleft = (0, 0)

                # Commencer l'animation du screamer
                screamer_start_time = pygame.time.get_ticks()  # Enregistrez le moment où l'animation du screamer commence
                darwinmp3.play()
                joueur.arreter_animation()
        

            # Obtenez le temps écoulé depuis le début de l'animation
            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - screamer_start_time

            # Alternez les couleurs de fond entre noir et rouge pendant l'animation du screamer
        
            if (elapsed_time // 250) % 2 == 0:
                background_color = (0, 0, 0)
            else:
                background_color = (255, 0, 0)
        
            window.fill(background_color)
            window.blit(images_scream[0], (150, 30))
            pygame.display.update()

            if elapsed_time > 2000:  # Arrêtez l'effet après 2 secondes (ajustez le temps si nécessaire)
                run = False
        elif not enemy.rect.colliderect(joueur.rect):
            enemy.deplacer(joueur)
            joueur.deplacer()
            window.blit(enemy.image, enemy.rect)  
            window.blit(joueur.image, joueur.rect)       
            
    if gagne:  
            font = pygame.font.Font("fonts/Minecraft.ttf", 72)
            texte = font.render("Partie gagnee !", True, (0, 0, 0))
            window.blit(texte, (1024 // 2 - texte.get_width() // 2, 768 // 2 - texte.get_height() // 2))
            joueur.arreter_animation()
            gameMusic.stop()
    else:
            filter = pygame.surface.Surface((1024, 768))
            filter.fill(pygame.color.Color('White'))
            filter.blit(lampe, (joueur.rect.centerx-200, joueur.rect.centery-200))
            window.blit(filter, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
def genererMur():
    
 while True:
    x = random.randint(0, 1024 - 28)
    y = random.randint(0, 768 - 20)
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

#main loop
genererMur()
while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    if(gamestate == GameState.INITIATING):
        #draw background
        initWindow(window,True)
        
        gamestate = GameState.WAITING_FOR_HISTORY
        
        
    elif(gamestate == GameState.WAITING_FOR_HISTORY):
        if startButton.isClicked():
            gamestate = GameState.HISTORY
            print("Start button clicked")
            pygame.mouse.set_pos(window_width/2, window_height/2)
        
    
    elif(gamestate == GameState.HISTORY):
        clear(window)
        drawHistory(window)
        gamestate = GameState.WAITING_FOR_CHARACTER
        
        
        
        
    elif(gamestate == GameState.WAITING_FOR_CHARACTER):    
        if startButton.isClicked():
            gamestate = GameState.CHARACTER  
            clear(window)
            #Afficher ta fenêtre
            drawCharacter(window)
        if returnButton.isClicked():
            initWindow(window,False) 
            gamestate = GameState.WAITING_FOR_HISTORY
            
    elif(gamestate == GameState.CHARACTER):
        
        if btnSprite1.isClicked():
            gamestate = GameState.PLAYING
            clear(window)
            joueur = Player(100, 100, 0)
        elif btnSprite2.isClicked():
            gamestate = GameState.PLAYING
            clear(window)
            joueur = Player(512, 354, 1)
        elif returnButton.isClicked():
            clear(window)
            drawHistory(window) 
            gamestate = GameState.WAITING_FOR_CHARACTER  
            pygame.mouse.set_pos(window_width/2, window_height/2)  
            
    elif gamestate == GameState.PLAYING:
        playingMod(window, joueur, gameloop)    
        gameloop += 1;    
        
    
    
        
    elif(gamestate == GameState.WAITING_FOR_START):    
        if startButton.isClicked():
            gamestate = GameState.START  
            print("Start button clicked") 
            pygame.mixer.music.stop()
    
    elif(gamestate == GameState.START):
        startGame(window)
        gamestate = GameState.PLAYING


    
    
            
      
        
    pygame.display.update()
        
pygame.quit()

