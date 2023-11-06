import pygame
from pygame.locals import *
from gamestate import GameState
from button import Button

#inits
pygame.init()
pygame.font.init()
pygame.mixer.init()

clock = pygame.time.Clock()
font = pygame.font.Font("fonts/Minecraft.ttf", 36)

#define dimensions
window_width = 1024
window_height = 768

#vars
gamestate = GameState.INITIATING
startButton = Button(window_width/2, window_height/1.25, pygame.image.load("assets/buttons/start.png"))

#create the window
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Save The Exams')

#Create landing text
text = font.render("Save The Exams", False, (255, 255, 255))
text_rect = text.get_rect()
text_rect.center = (window_width/2, window_width/4)

#starting background
startingBackground = pygame.image.load("assets/bg/startbg.png")
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


#main loop

while run:
    clock.tick(60)
    
    if(gamestate == GameState.INITIATING):
        #draw background
        window.blit(startingBackground, (0, 0))
        window.blit(text, text_rect)
        startButton.draw(window)
        pygame.mixer.music.play()
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

