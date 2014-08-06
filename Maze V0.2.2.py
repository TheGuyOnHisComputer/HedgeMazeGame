#-------------------------------------------------------------------------------
# Name:        Hedge BEV Game
# Purpose:
#
# Author:      ahawley
#
# Created:     08/01/2014
# Copyright:   (c) ahawley 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import pygame, time, sys
from pygame.locals import *
import random

#Player start cords
x=0
y=0


FPS = 15
WINDOWWIDTH = 800
WINDOWHEIGHT = 600
CELLSIZE = 20
assert WINDOWWIDTH % CELLSIZE == 0
assert WINDOWHEIGHT % CELLSIZE == 0
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)
CURRENTLEVEL = 0

#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
DARKPINK  = (255,  20, 147)
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
ORANGE    = (255, 153,  18)
DARKGRAY  = ( 40,  40,  40)
YELLOW    = (255, 255,   0)
BLUE      = (  0,   0, 255)
KHAKI     = (139, 134,  78)
BGCOLOR = BLACK


UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'



def main():
    pygame.display.init()
    global FPSCLOCK, wn, BASICFONT, level
    pygame.init()
    level = 1
    FPSCLOCK = pygame.time.Clock()
    wn = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.SysFont('ActionIsShaded', 24)
    pygame.display.set_caption('Hedge Maze')
    print("Pre-show start screen: success")

    showStartScreen()
    runGame()

def runGame():
    print("Key Pressed")
    clearScreen()
    levelStartScreen()
    time.sleep(3)
    loadlevel1()
    time.sleep(3)
    #terminate()

def showStartScreen():
    global titleFont
    titleFont = pygame.font.SysFont('ActionIsShaded', 100)
    titleSurf1 = titleFont.render('Hedge Maze', True, WHITE, RED)
    degrees1 = 0
    print("Pre-loop show start screen: success")
    while True:
        wn.fill(BGCOLOR)
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        wn.blit(rotatedSurf1, rotatedRect1)
        drawPressKeyMsg()
        if checkForKeyPress():
            pygame.event.get()
            return
        pygame.display.update()
        degrees1 += 1
        print("End of showstartscreen loop: success")
        time.sleep(0.02)

def levelStartScreen():
    levelNameSurf1 = titleFont.render('Level ' + str(level), True, RED, WHITE)
    levelNameRect1 = levelNameSurf1.get_rect()
    levelNameRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT * 0.25)
    wn.blit(levelNameSurf1, levelNameRect1)
    pygame.display.update()

def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press a key to play.', True, DARKGRAY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    wn.blit(pressKeySurf, pressKeyRect)

def terminate():
    pygame.quit()

def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key

def drawGrid():
    global vertline
    for x in range(0, WINDOWWIDTH, CELLSIZE): # draw vertical lines
        pygame.draw.line(wn, WHITE, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE): # draw horizontal lines
        vertline = pygame.draw.line(wn, WHITE, (0, y), (WINDOWWIDTH, y))
    pygame.display.update()

def clearScreen():
    wn.fill(BGCOLOR)
    pygame.display.update()



class hedgeTexture:
    def __init__(self):
        self.y = 0
        self.x = 0

    def loadTexture(self):
        self.texture = pygame.image.load("hedge texture.gif")
        self.texturerect = self.texture.get_rect()
        self.coords = (random.randrange(CELLSIZE, WINDOWWIDTH, CELLSIZE), random.randrange(CELLSIZE, WINDOWHEIGHT, CELLSIZE))
        self.texturerect.move_ip(self.coords)
        wn.blit(self.texture, self.texturerect)
        pygame.display.flip()

    def loadTextureRow(self, x, y, r):
        while x<r:
            self.texture = pygame.image.load("hedge texture.gif")
            self.texturerect = self.texture.get_rect()
            self.coords = (x, y)
            self.texturerect.move_ip(self.coords)
            wn.blit(self.texture, self.texturerect)
            x += CELLSIZE

    def loadTextureCol(self, x, y, r):
        while y<r:
            self.texture = pygame.image.load("hedge texture.gif")
            self.texturerect = self.texture.get_rect()
            self.hedgecoords = (x, y)
            self.texturerect.move_ip(self.coords)
            wn.blit(self.texture, self.texturerect)
            y += CELLSIZE

class playerTexture:
    def __init__(self):
        self.y = 10
        self.x = 10
    def loadplayer(self, x, y):
        self.texture = pygame.image.load("You texture.gif")
        self.texturerect = self.texture.get_rect()
        self.coords = (x, y)
        self.texturerect.move_ip(self.coords)
        wn.blit(self.texture, self.texturerect)


        pygame.display.flip()

#Level Create

def loadlevel1():
    CURRENTLEVEL = 1
    count = 0
    nofhedges = 300
    hedges = 0
    global hedge1, hedgecoords
    clearScreen()
    drawGrid()
    player1 = playerTexture()
    player1.loadplayer(x, y)
    hedgecoords = []
    while hedges<nofhedges:
        hedge1 = hedgeTexture()
        hedge1.loadTexture()
        hedgecoords.insert(0, hedge1.coords)
        if ((WINDOWWIDTH/2)-(0.5*CELLSIZE), ((WINDOWHEIGHT/2)-(0.5*CELLSIZE))) in hedgecoords:
            hedges-1
        elif ((WINDOWWIDTH/2)+(0.5*CELLSIZE), ((WINDOWHEIGHT/2)+(0.5*CELLSIZE))):
            hedges-1
        elif ((WINDOWWIDTH/2)-(0.5*CELLSIZE), ((WINDOWHEIGHT/2)+(0.5*CELLSIZE))):
            hedges-1
        elif ((WINDOWWIDTH/2)+(0.5*CELLSIZE), ((WINDOWHEIGHT/2)-(0.5*CELLSIZE))):
            hedges-1
        hedges+=1
        count +=1
    direction(x, y)

def direction(x, y):
    direction = RIGHT
    while True: # main game loop
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a):
                    direction = LEFT
##                    print("Left")
                    if (x,y) in hedgecoords:
                        print("Woops! That was a hedge you walked into; you're stuck! Level Restarting....")
                        time.sleep(2)
                        loadlevel1()
                    elif x>CELLSIZE-1:
                        x-=CELLSIZE
                    else:
                        print("Out of play")
                elif (event.key == K_RIGHT or event.key == K_d):
                    direction = RIGHT
##                    print("Right")
                    if (x,y) in hedgecoords:
                        print("Woops! That was a hedge you walked into; you're stuck! Level Restarting....")
                        time.sleep(2)
                        loadlevel1()
                    elif x<WINDOWWIDTH+1:
                        x+=CELLSIZE
                    else:
                        print("Out of play")
                elif (event.key == K_UP or event.key == K_w):
                    direction = UP
##                    print("Up")
                    if (x,y) in hedgecoords:
                        print("Woops! That was a hedge you walked into; you're stuck! Level Restarting....")
                        time.sleep(2)
                        loadlevel1()
                    elif y>CELLSIZE-1:
                        y-=CELLSIZE
                    else:
                        print("Out of play")
                elif (event.key == K_DOWN or event.key == K_s):
##                    print("Down")
                    direction = DOWN
                    if (x,y) in hedgecoords:
                        print("Woops! That was a hedge you walked into; you're stuck! Level Restarting....")
                        time.sleep(2)
                        loadlevel1()
                    elif y<561:
                        y=y+CELLSIZE
                    else:
                        print("Out of play")
                elif event.key == K_ESCAPE:
                    terminate()
        player1 = playerTexture()
        player1.loadplayer(x, y)

main()
