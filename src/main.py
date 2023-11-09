import pygame
from pygame.locals import *
from gamestate import GameState
from button import Button
from player import Player
from enemy import Enemy
import random #pour generer la position x et y des objets de manière aléatoire
from usb import CleUSB
from mur import Mur,WallLaby
import time #pour gerer le rythme
import argparse

parser = argparse.ArgumentParser(description='Jeu "Save The Exams"')
parser.add_argument('-l', '--lampe', action='store_true', help='Desactive la lampe torche')
parser.add_argument('-d', '--difficile', action='store_true', help='Diminue la tolérence d\'erreur du timing (0.12ms)')
parser.add_argument('-f', '--facile', action='store_true', help='Augmente la tolérence d\'erreur du timing (0.05ms)')
parser.add_argument('-g', '--god', action='store_true', help='Seulement si vous avez le rythme dans la peau ! (0.03ms)')


args = parser.parse_args()
not_use_torch = args.lampe
hard_timing = args.difficile
ez_timing = args.facile
god_timing = args.god


pygame.init()
pygame.font.init()
pygame.mixer.init()

clock = pygame.time.Clock()

font = pygame.font.Font("fonts/Minecraft.ttf", 72)
subfont = pygame.font.Font("fonts/Minecraft.ttf", 36)
favicon = pygame.image.load("assets/favicon/favicon.png")
pygame.display.set_icon(favicon)

#sol de l'iut et lampe torche
image_bg = pygame.image.load("assets/bg/bg.png")

lampe = pygame.image.load('assets/elements/circle200.png')


#dimensions de la fenetre
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


gamestate = GameState.INITIATING
startButton = Button(window_width/2, window_height/1.25, pygame.image.load("assets/buttons/start.png"))
creditButton = Button(window_width/2, window_height/1.10, pygame.image.load("assets/buttons/credits.png"))
endButton = Button(window_width/2, window_height/1.25, pygame.image.load("assets/buttons/accueil.png"))
returnButton = Button(75,window_height - 50, pygame.image.load("assets/buttons/arrow.png"))
btnFlipper = Button(window_width/4, window_height/2, pygame.image.load("assets/buttons/btnflipper.png"))
btnLaby = Button(window_width/2, window_height/2, pygame.image.load("assets/buttons/btnlaby.png"))

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

#gestion du nombre d'ennemis
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

#parametres de gestion du rythme
BPM = 124 #battements par seconde de la musique du jeu
BEAT_INTERVAL = 60 / BPM  # Intervalle entre les battements par secondes 



if hard_timing:
    BEAT_TOLERANCE = 0.05  # Tolerance de mauvais timing
elif ez_timing:
   BEAT_TOLERANCE = 0.12
elif god_timing:
    BEAT_TOLERANCE = 0.03
else:
    BEAT_TOLERANCE = 0.08 

key_pressed = False
last_beat_time = pygame.time.get_ticks() / 1000 - BEAT_INTERVAL
error_count = 0 #nombre d'erreurs de timing autorisé
screamer_start_time = 0
darwinmp3 = pygame.mixer.Sound("assets/sounds/game_over/darwin.mp3")
gameMusic = pygame.mixer.Sound("assets/sounds/musics/game_theme.ogg")
click = pygame.mixer.Sound("assets/sounds/menus/click.mp3")
gagne =False

window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Save The Exams')

#charger le bg en loop (idée abandonnée car peu interessante)
startingBackground = pygame.image.load("assets/bg/loop.jpg")


ingameBackground = pygame.image.load("assets/bg/bg.png")
start = pygame.mixer.Sound("assets/sounds/musics/starting.ogg")
# Labyrinthe
level = []
cle_usbLabby = CleUSB(920, 650)

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
    creditButton.draw(window)

        
def drawHistory(window):
    titlefont = pygame.font.Font("fonts/Minecraft.ttf",25)
    infofont = pygame.font.Font("fonts/Minecraft.ttf", 17)
    
    titlefont = pygame.font.Font("fonts/Minecraft.ttf",25)
    infofont = pygame.font.Font("fonts/Minecraft.ttf", 17)
    
    historymessages = ["Vous venez de lamentablement foirer vos partiels de mi-",
                "semestre, et la suite semble mal embarquee :/",
                "Votre derniere chance ?",
                "Obtenir 20/20 a tous les examens de la prochaine semaine de partiels !",
                "Alors que vous aviez abandonne tout espoir, une rumeur",
                "commence a se propager dans l'IUT: il existerait une clef USB ",
                "secrete dans le bureau 101, regroupant l'integralite des",
                " prochains examens...",
                "Votre objectif ?",
                "Muni d'une lampe torche, vous infiltrez l'IUT de nuit pour ",
                "recuperer la fameuse clef. Mais attention, des choses etranges",
                "se produisent en dehors des heures d'ouverture...",
    ]
    clear(window)
    window.fill((0, 0, 0))
    historyheight = 120
    historytitle = titlefont.render("HISTOIRE",False,(255,255,255))
    historytitle_rect = historytitle.get_rect()
    historytitle_rect.center = (window_width/3,historyheight -50 ) 
    window.blit(historytitle,historytitle_rect)
    
    rulesmessages = ["Cherchez la clef USB a l'aide des",
                     "fleches directionnelles du ",
                     "clavier, esquivez les professeurs",
                     "et suivez le rthme de la",
                     "musique pour camoufler vos pas",
                     "et ne pas vous faire reperer !"]
    

    
    for i in range(len(historymessages)):
        
        historytext = infofont.render(historymessages[i], False, (255, 255, 255))
        historytext_rect = historytext.get_rect()
        historytext_rect.center = (window_width /3, historyheight)
        window.blit(historytext, historytext_rect)
        historyheight += 30
        
    historyheight = 120
    rulestitle = titlefont.render("REGLES",False,(255,255,255))
    rulestitle_rect = rulestitle.get_rect()
    rulestitle_rect.center = (window_width/1.25,historyheight -50 ) 
    window.blit(rulestitle,rulestitle_rect)  
    
    for i in range(len(rulesmessages)):
        
        rulestext = infofont.render(rulesmessages[i], False, (255, 255, 255))
        rulestext_rect = rulestext.get_rect()
        rulestext_rect.center = (window_width /1.25, historyheight)
        window.blit(rulestext, rulestext_rect)
        historyheight += 30
          
    returnButton.draw(window)
    startButton.draw(window) 
    
def drawCredits(window):
    creditlist = [[pygame.image.load("assets/credits/gabriel128circle.png"),"Gabriel SCHAAL","Game designer & developer"],
                  [pygame.image.load("assets/credits/ilan128circle.png"),"Ilan DARMON","Artist & developer"],
                  [pygame.image.load("assets/credits/yanis128circle.png"),"Yanis HARKATI","Menu designer & developer"],
                  [pygame.image.load("assets/credits/antoine.png"), "Antoine HUGUET", "Animator"]
                 ]

    musics = ["https://www.youtube.com/watch?v=CqJ95-zjvK0","https://www.youtube.com/watch?v=uQbzK4OROjQ", "https://pixabay.com", "Herve Blanchon"]
    images = ["https://www.pixelicious.xyz", "https://www.dafont.com/fr/minecraft.font"]
    infofont = pygame.font.Font("fonts/Minecraft.ttf", 15)
    titlefont = pygame.font.Font("fonts/Minecraft.ttf", 27)
    subtitlefont = pygame.font.Font("fonts/Minecraft.ttf", 22)
    
    sourcetitle = titlefont.render("Sources", False, (255, 255, 255))
    source_title_rect = sourcetitle.get_rect()
    source_title_rect.center = (window_width/2, window_height/1.70)
    
    musicsubtitle = subtitlefont.render("Audios", False, (255, 255, 255))
    musicsubtitle_rect = musicsubtitle.get_rect()
    musicsubtitle_rect.center = (window_width/1.4, window_height/1.45)
    
    imagessubtitle = subtitlefont.render("Visuels", False, (255, 255, 255))
    imagessubtitle_rect = imagessubtitle.get_rect()
    imagessubtitle_rect.center = (294, window_height/1.45)
    
    
    clear(window)
    window.fill((0, 0, 0))
    historyheight = 120
    width = 175
    for i in range(len(creditlist)):
        currentimg = creditlist[i][0]
        currentname = infofont.render(creditlist[i][1], False, (255, 255, 255))
        currentrole = infofont.render(creditlist[i][2], False, (255, 255, 255))
        

        currentname_rect = currentname.get_rect()
        currentrole_rect = currentrole.get_rect()

        
        currentname_rect.center = (width, window_height/2.25)
        currentrole_rect.center = (width,  window_height/2.15)
        
        window.blit(currentimg, (width-60, window_height/5))
        window.blit(currentname, currentname_rect)
        window.blit(currentrole, currentrole_rect)
        historyheight += 30
        width += 240
        
    window.blit(sourcetitle, source_title_rect)
    window.blit(musicsubtitle, musicsubtitle_rect)
    window.blit(imagessubtitle, imagessubtitle_rect)
    
    for i in range(len(musics)):
        currentmusic = infofont.render(musics[i], False, (255, 255, 255))
        currentmusic_rect = currentmusic.get_rect()
        currentmusic_rect.center = (window_width/1.4, window_height/1.35 + i*30)
        window.blit(currentmusic, currentmusic_rect)
    
    for i in range(len(images)):
        currentimage = infofont.render(images[i], False, (255, 255, 255))
        currentimage_rect = currentimage.get_rect()
        currentimage_rect.center = (294, window_height/1.35 + i*30)
        window.blit(currentimage, currentimage_rect)    
    returnButton.draw(window)  
    
    
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
    global screamer_start_time
    global run
    global gagne
    global key_pressed
    global last_beat_time
    global error_count
    global start_time
    clear(window)  
    start.stop()
    if gameloop == 0:
        gameMusic.play()
    joueur.deplacer()
    
    if event.type == pygame.KEYDOWN and not key_pressed and not gagne:
                key_pressed = True
                start_time = time.time()  # Enregistre le temps auquel la touche a été enfoncée
                if (event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):
                    
                    current_time = time.time()
                    if current_time - last_beat_time >= BEAT_INTERVAL - BEAT_TOLERANCE and current_time - last_beat_time <= BEAT_INTERVAL + BEAT_TOLERANCE and error_count < 2:
                        
                        print("Bon timing")
                        joueur.deplacer()       
                        if cle_usb.check_collision(joueur):
                            print("Partie gagnée")
                            gagne = True        
                            return GameState.VICTORY
                    else:
                        error_count += 1
                        print("Mauvais timing")
  
                    if error_count >= 2:
                        return GameState.LOSER

                    last_beat_time = current_time
    elif event.type == pygame.KEYUP:
        key_pressed = False
        start_time = None
                
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
    
    
    
    for enemy in ennemies:
        for mur in murs:
            if enemy.rect.colliderect(mur.rect):
                overlap_x = enemy.rect.width / 2 + mur.rect.width / 2 - abs(enemy.rect.centerx - mur.rect.centerx)
                overlap_y = enemy.rect.height / 2 + mur.rect.height / 2 - abs(enemy.rect.centery - mur.rect.centery)

                if overlap_x < overlap_y:
                    if enemy.rect.centerx < mur.rect.centerx:
                        enemy.rect.right = mur.rect.left
                    else:
                        enemy.rect.left = mur.rect.right
                else:
                    if enemy.rect.centery < mur.rect.centery:
                        enemy.rect.bottom = mur.rect.top
                    else:
                        enemy.rect.top = mur.rect.bottom
        if enemy.rect.colliderect(joueur.rect):
        
            if screamer_start_time == 0:
                # En cas de collision, réinitialise les positions des personnages en haut à gauche
                joueur.rect.topleft = (0, 0)
                enemy.rect.topleft = (0, 0)

                # Commence l'animation du screamer
                screamer_start_time = pygame.time.get_ticks()  # Enregistre le moment où l'animation du screamer commence
                gameMusic.stop()
                darwinmp3.play()
                joueur.arreter_animation()
        

            #le temps écoulé depuis le début de l'animation
            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - screamer_start_time

            # Alterne les couleurs de fond entre noir et rouge pendant l'animation du screamer
        
            if (elapsed_time // 250) % 2 == 0:
                background_color = (0, 0, 0)
            else:
                background_color = (255, 0, 0)
        
            window.fill(background_color)
            window.blit(images_scream[0], (150, 30))
            pygame.display.update()

            if elapsed_time > 2000:  # Arrêter l'effet après 2 secondes (ajuster le temps si nécessaire)
                
                return GameState.LOSER
        elif not enemy.rect.colliderect(joueur.rect):
            enemy.deplacer(joueur)
            window.blit(enemy.image, enemy.rect)  
            window.blit(joueur.image, joueur.rect)       

    if gagne:  
            
            font = pygame.font.Font("fonts/Minecraft.ttf", 72)
            #texte = font.render("Partie gagnee !", True, (0, 0, 0))
           # window.blit(texte, (1024 // 2 - texte.get_width() // 2, 768 // 2 - texte.get_height() // 2))
            joueur.arreter_animation()
            gameMusic.stop()
    else: #code pour activer/desactiver la lampe torche
        if not not_use_torch:
            filter = pygame.surface.Surface((1024, 768))
            filter.fill(pygame.color.Color('White'))
            filter.blit(lampe, (joueur.rect.centerx-200, joueur.rect.centery-200))
            window.blit(filter, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
    return GameState.PLAYING    
def iterate(line):
    for column_number, block in enumerate(line):
        yield column_number, block
        
def genererLabyLevel():
    global level
    with open("assets/labyrinthe/level.txt") as level_file:
        line_file = level_file.readline()
        line_number = 0
        while line_file:
            for column_number, block in iterate(line_file):
                if block == "+":
                    level.append(WallLaby(line_number, column_number))
            line_file = level_file.readline()
            line_number += 1
            
def playingModLabyrinthe(window,joueur,gameloop):
    global gagne
    global font
    global key_pressed
    global error_count
    global last_beat_time
    global start_time
    start.stop()
    if gameloop == 0:
        gameMusic.play()
    joueur.deplacer()
    clear(window)
    

    if event.type == pygame.KEYDOWN and not key_pressed and not gagne:
                key_pressed = True
                start_time = time.time()  # Enregistre le temps auquel la touche a été enfoncée
                if (event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):
                    
                    current_time = time.time()
                    if current_time - last_beat_time >= BEAT_INTERVAL - BEAT_TOLERANCE and current_time - last_beat_time <= BEAT_INTERVAL + BEAT_TOLERANCE and error_count < 2:
                        
                        print("Bon timing")
                        joueur.deplacer()       
                        if cle_usbLabby.check_collision(joueur):
                            print("Partie gagnée")
                            gagne = True        
                            return GameState.VICTORY
                    else:
                        error_count += 1
                        print("Mauvais timing")
  
                    if error_count >= 2:
                        return GameState.LOSER

                    last_beat_time = current_time
    elif event.type == pygame.KEYUP:
        key_pressed = False
        start_time = None
    
    
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
    window.blit(image_bg, (0, 0))
    for wall in level:
        pygame.draw.rect(window, (0, 0, 0), wall.rect)
    window.blit(joueur.image, joueur.rect.topleft)
    
   
        
        
    
    
    window.blit(cle_usbLabby.image, cle_usbLabby.rect)    
    if gagne:
        font = pygame.font.Font("fonts/Minecraft.ttf", 72)
        texte = font.render("Partie gagnee !", True, (0, 0, 0))
        
        window.blit(texte, (330 , 420))
            
        joueur.arreter_animation()
    else: #code pour activer/desactiver la lampe torche
        filter = pygame.surface.Surface((1024, 768))
        filter.fill(pygame.color.Color('White'))
        filter.blit(lampe, (joueur.rect.centerx-200, joueur.rect.centery-200))
        window.blit(filter, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
    return GameState.PLAYINGLABY    
#remise des parametres du jeu à leur etat initial en cas de restart
def reset_game():
    global screamer_start_time, run, gagne, key_pressed, last_beat_time, error_count, gameloop,ennemies
    screamer_start_time = 0
    run = True
    gagne = False
    key_pressed = False
    last_beat_time = pygame.time.get_ticks() / 1000 - BEAT_INTERVAL
    error_count = 0
    gameloop = 0
    ennemies = [
        Enemy(800, 334, images),
        Enemy(700, 500, images),
        Enemy(600, 200, images),
        Enemy(200, 500, images),
        Enemy(700, 800, images),
        Enemy(300, 500, images),
        Enemy(400, 600, images),
        Enemy(400, 200, images)
    ]
    genererMur()
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

def choosemap():
    clear(window)
    window.blit(startingBackground, (0, 0))
    title = font.render("Choisissez votre map", False, (255, 255, 255))
    title_rect = title.get_rect()
    title_rect.center = (window_width/2, window_height/4)
    window.blit(title, title_rect)
    btnFlipper.draw(window)
    btnLaby.draw(window)
    returnButton.draw(window)
    

        
    
#main loop
genererMur()
genererLabyLevel() 
while run:
   
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    if(gamestate == GameState.INITIATING):
        
        initWindow(window,True)
        
        gamestate = GameState.WAITING_FOR_HISTORY
        
        
    elif(gamestate == GameState.WAITING_FOR_HISTORY):
        if startButton.isClicked():
            gamestate = GameState.HISTORY
            click.play()
           
            pygame.mouse.set_pos(window_width/2, window_height/2)
        elif creditButton.isClicked():
            gamestate = GameState.CREDITS
            click.play()
            
    elif(gamestate == GameState.CREDITS):
        drawCredits(window)
        if returnButton.isClicked():
            initWindow(window,False) 
            gamestate = GameState.WAITING_FOR_HISTORY
            click.play()
    
    elif(gamestate == GameState.HISTORY):
        clear(window)
        drawHistory(window)
        gamestate = GameState.WAITING_FOR_CHARACTER
        
        
        
        
    elif(gamestate == GameState.WAITING_FOR_CHARACTER):    
        if startButton.isClicked():
            gamestate = GameState.CHARACTER  
            
            #Afficher ta fenêtre
            drawCharacter(window)
            click.play()
            
        if returnButton.isClicked():
            initWindow(window,False) 
            gamestate = GameState.WAITING_FOR_HISTORY
            click.play()
            
    elif(gamestate == GameState.CHARACTER):
        clear(window)
        drawCharacter(window)
        gamestate = GameState.WAITING_FOR_CHOOSE_MAP
       
    
    elif gamestate == GameState.WAITING_FOR_CHOOSE_MAP:
        if btnSprite1.isClicked():
            gamestate = GameState.CHOOSE_MAP
            clear(window)
            joueur = Player(100, 100, 0)
            click.play()
            #murs = appendMurs(nb_murs)
        elif btnSprite2.isClicked():
            gamestate = GameState.CHOOSE_MAP
            clear(window)
            joueur = Player(100, 100, 1)
            click.play()
            #murs = appendMurs(nb_murs)
        elif returnButton.isClicked():
            clear(window)
            drawHistory(window) 
            gamestate = GameState.WAITING_FOR_CHARACTER  
            pygame.mouse.set_pos(window_width/2, window_height/2)  
            click.play()

            
                 
    elif gamestate == GameState.PLAYING:
        gamestate = playingMod(window, joueur, gameloop)    
        gameloop += 1;    
        if gamestate == GameState.VICTORY or gamestate == GameState.LOSER:
            reset_game()
            
    elif gamestate == GameState.PLAYINGLABY:
        gamestate = playingModLabyrinthe(window, joueur, gameloop)    
        gameloop += 1;    
        if gamestate == GameState.VICTORY or gamestate == GameState.LOSER:
            reset_game()        
            
    elif gamestate == GameState.CHOOSE_MAP:
        choosemap()  
        gamestate = GameState.WAITING_FOR_MAP   
        #pygame.mouse.set_pos(window_width/2, window_height/2)
        
    elif gamestate == GameState.WAITING_FOR_MAP:
        if btnFlipper.isClicked():
            gamestate = GameState.START
            print("Start button clicked")
            pygame.mouse.set_pos(window_width/2, window_height/2)
        elif btnLaby.isClicked():
            gamestate = GameState.STARTLABY
            print("Start button clicked")
            pygame.mouse.set_pos(window_width/2, window_height/2)  
        elif returnButton.isClicked():
            print("Return button clicked")     
    
    
        
    elif(gamestate == GameState.WAITING_FOR_START):    
        if startButton.isClicked():
            gamestate = GameState.START  
            print("Start button clicked") 
            click.play()
            pygame.mixer.music.stop()
    
    elif(gamestate == GameState.START):
        startGame(window)
        gamestate = GameState.PLAYING
        
    elif(gamestate == GameState.STARTLABY):
        startGame(window)
        gamestate = GameState.PLAYINGLABY
            

        

    elif(gamestate == GameState.VICTORY):   
         
        texte = font.render("Partie gagnee !", True, (255, 255, 255))
        window.blit(texte, (1024 // 2 - texte.get_width() // 2, 768 // 2 - texte.get_height() // 2))
        joueur.arreter_animation()
        endButton.draw(window)
        gameMusic.stop()    
        gamestate = GameState.WAITING_FOR_REDO
        
    elif(gamestate == GameState.WAITING_FOR_REDO):
        if endButton.isClicked():
            gamestate = GameState.INITIATING
            print("End button clicked")
            pygame.mouse.set_pos(window_width/2, window_height/2) 
            click.play()
    
    elif(gamestate == GameState.LOSER):
        texte = font.render("Partie perdue !", True, (255, 255, 255))
        window.blit(texte, (1024 // 2 - texte.get_width() // 2, 768 // 5 - texte.get_height() // 2))
        joueur.arreter_animation()
        endButton.draw(window)
        gameMusic.stop()    
        gamestate = GameState.WAITING_FOR_REDO

          
    pygame.display.update()
        
pygame.quit()