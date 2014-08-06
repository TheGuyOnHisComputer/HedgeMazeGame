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
WINDOWWIDTH = 600
WINDOWHEIGHT = 600
CELLSIZE = 20
assert WINDOWWIDTH % CELLSIZE == 0
assert WINDOWHEIGHT % CELLSIZE == 0
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

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
    for x in range(0, WINDOWWIDTH, CELLSIZE): # draw vertical lines
        pygame.draw.line(wn, WHITE, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE): # draw horizontal lines
        pygame.draw.line(wn, WHITE, (0, y), (WINDOWWIDTH, y))
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
        self.coords = (random.randrange(20, 600, 20), random.randrange(20, 600, 20))
        self.texturerect.move_ip(self.coords)
        wn.blit(self.texture, self.texturerect)

        pygame.display.flip()

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



def loadlevel1():
    clearScreen()
    drawGrid()
    player1 = playerTexture()
    player1.loadplayer(x, y)
    hedges=0
    while hedges<250:
        hedge1 = hedgeTexture()
        hedge1.loadTexture()
        hedges=hedges+1
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
                    print("Left")
                    if x>19:
                        x=x-20
                    else:
                        print("Out of play")
                elif (event.key == K_RIGHT or event.key == K_d):
                    direction = RIGHT
                    print("Right")
                    if x<561:
                        x=x+20
                    else:
                        print("Out of play")
                elif (event.key == K_UP or event.key == K_w):
                    direction = UP
                    print("Up")
                    if y>19:
                        y=y-20
                    else:
                        print("Out of play")
                elif (event.key == K_DOWN or event.key == K_s):
                    print("Down")
                    direction = DOWN
                    if y<561:
                        y=y+20
                    else:
                        print("Out of play")
                elif event.key == K_ESCAPE:
                    terminate()
        player1 = playerTexture()
        player1.loadplayer(x, y)

main()
