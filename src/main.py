import pygame
from pygame.locals import *
from gamestate import GameState
from button import Button
from player import Player

#inits
pygame.init()
pygame.font.init()
pygame.mixer.init()

clock = pygame.time.Clock()
font = pygame.font.Font("fonts/Minecraft.ttf", 72)
subfont = pygame.font.Font("fonts/Minecraft.ttf", 36)
favicon = pygame.image.load("assets/favicon/favicon.png")
pygame.display.set_icon(favicon)

#define dimensions
window_width = 1024
window_height = 768

#vars
gamestate = GameState.INITIATING
startButton = Button(window_width/2, window_height/1.25, pygame.image.load("assets/buttons/start.png"))
#bouton pour choisir genre
btnSprite1 = Button(303, 520.4, pygame.image.load("assets/buttons/btnsprite.png"))
btnSprite2 = Button(702, 520.4, pygame.image.load("assets/buttons/btnsprite.png"))
startingtext = font.render("Save The Exams", False, (255, 255, 255))
subtitle =  subfont.render("Infiltrez vous a l'IUT 2 pour sauver vos partiels", False, '#d3d3d3')
iutlogo = pygame.image.load("assets/iut2logo_1.png")
startingtext_rect = startingtext.get_rect()
startingsubtext_rect = subtitle.get_rect()
startingtext_rect.center = (window_width/2, window_height/4)
startingsubtext_rect.center = (window_width/2, window_height/3)

#create the window
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Save The Exams')



#starting background
startingBackground = pygame.image.load("assets/bg/loop.jpg")
#ingame background
ingameBackground = pygame.image.load("assets/bg/bg.png")
pygame.mixer.music.load("assets/sounds/musics/starting.ogg")



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
    
def initWindow(window):
    window.blit(startingtext, startingtext_rect)
    startButton.draw(window)
    pygame.mixer.music.play()
        
        
def drawHistory(window):
    infofont = pygame.font.Font("fonts/Minecraft.ttf", 20)
    messages = ["Vous venez de lamentablement foirer vos partiels de",
                "mi- semestre, et la suite semble mal embarquee :/",
                "Votre derniere chance ?",
                "",
                "Obtenir 20/20 a tous les",
                "examens de la prochaine semaine de partiels !",
                "Alors que vous aviez abandonne tout espoir,",
                "une rumeur commence a se propager dans l'IUT:",
                "Il existerait une clef USB secrete dans le bureau 101,",
                "regroupant l'integralite des prochains examens...",
                "Votre objectif ? Equipe d'une lampe torche, vous ",
                "infiltrez l'IUT de nuit pour recuperer la fameuse clef.",
                "Mais attention, des choses etranges se produisent",
                "en dehors des heures d'ouverture..."]
    clear(window)
    window.fill((0, 0, 0))
    historyheight = 120
    for i in range(len(messages)):
        
        historytext = infofont.render(messages[i], False, (255, 255, 255))
        historytext_rect = historytext.get_rect()
        historytext_rect.center = (window_width/2, historyheight)
        window.blit(historytext, historytext_rect)
        historyheight += 30
        
    startButton.draw(window) 
    
def drawCharacter(window) :
    fontsprite = pygame.font.Font("fonts/Minecraft.ttf", 26)


    BLACK = (0, 0, 0)
    text = font.render("Faites votre choix", False, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.center = (window_width/2, window_height/4 -100)
    

    textsprite1 = fontsprite.render("Sprite 1", False, (255, 255, 255))
    textsprite1_rect = textsprite1.get_rect()
    textsprite1_rect.center = (310,494.4)

    textsprite2 = fontsprite.render("Sprite 2", False, (255, 255, 255))
    textsprite2_rect = textsprite1.get_rect()
    textsprite2_rect.center = (707, 494.4)

    imagesprite1 = pygame.image.load("assets/player/Player0.png")
    imagesprite2 = pygame.image.load("assets/playerFemale/PlayerFemale0.png")

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
    window.blit(textsprite1, textsprite1_rect)
    window.blit(textsprite2, textsprite2_rect)
    
    

def playingMod(window,joueur) :
    clear(window)  
    window.blit(joueur.image,joueur.rect)
    
    joueur.deplacer()
        


#main loop

while run:
    clock.tick(60)
    
    if(gamestate == GameState.INITIATING):
        #draw background
        initWindow(window)
        compteur_bg = 0
        window.blit(startingBackground.subsurface(Rect(0, 0, 1024, 968)), (0, 0))
        window.blit(subtitle, startingsubtext_rect)
        window.blit(iutlogo, (window_width/2, window_height/2))
        gamestate = GameState.WAITING_FOR_HISTORY
        
        
    elif(gamestate == GameState.WAITING_FOR_HISTORY):
        compteur_bg += 968
        if compteur_bg == 17424:
            compteur_bg = 0
        window.blit(startingBackground.subsurface(Rect(0, compteur_bg, 1024, 968)), (0, 0))
        window.blit(startingtext, startingtext_rect)
        window.blit(iutlogo, (window_height/2, window_height/2))
        window.blit(subtitle, startingsubtext_rect)
        startButton.draw(window) 

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
            
    elif(gamestate == GameState.CHARACTER):
        
        if btnSprite1.isClicked():
            gamestate = GameState.PLAYING
            clear(window)
            joueur = Player(512, 334, 0)
        elif btnSprite2.isClicked():
            gamestate = GameState.PLAYING
            clear(window)
            joueur = Player(512, 354, 1)
            
    elif gamestate == GameState.PLAYING:
        playingMod(window, joueur)        
        
    
    
        
    elif(gamestate == GameState.WAITING_FOR_START):    
        if startButton.isClicked():
            gamestate = GameState.START  
            print("Start button clicked") 
            pygame.mixer.music.stop()
    
    elif(gamestate == GameState.START):
        startGame(window)
        gamestate = GameState.PLAYING


    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
      
        
    pygame.display.update()
        
pygame.quit()

