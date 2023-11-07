import pygame
from pygame.locals import *
from gamestate import GameState
from button import Button

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
                "mi- semestre, et la suite semble mal embarquée :/",
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
        
        historytext = font.render(messages[i], False, (255, 255, 255))
        historytext_rect = historytext.get_rect()
        historytext_rect.topright = (window_width/2, historyheight)
        window.blit(historytext, historytext_rect)
        historyheight += 30
        
    startButton.draw(window) 
    
   





        


#main loop

while run:
    clock.tick(60)
   
    if(gamestate == GameState.INITIATING):
        #draw background
        initWindow(window)
        compteur_bg = 0
        window.blit(startingBackground.subsurface(Rect(0, 0, 1024, 968)), (0, 0))
        window.blit(subtitle, startingsubtext_rect)
        window.blit(iutlogo, (window_width, 50))
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
        gamestate = GameState.WAITING_FOR_START
           
        
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

