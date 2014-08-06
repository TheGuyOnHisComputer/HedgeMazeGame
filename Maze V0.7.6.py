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


"""
TO DO:
    -Fix Life System(Refreshing full after every load of map)
    -Instant recognition(goal)
    -Highscores system
"""

#Imports
import pygame, time, sys
from pygame.locals import *
import random

#Player start cords
x=0
y=0

#Amount of Hedges In Level 1
nofhedges = 50

#Initial Global Variables
timer = 10
level = 1

#Not currently implemented
FPS = 15

WINDOWWIDTH = 800
WINDOWHEIGHT = 600
CELLSIZE = 20
assert WINDOWWIDTH % CELLSIZE == 0
assert WINDOWHEIGHT % CELLSIZE == 0
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)
COLLISIONMESSAGE = "Woops! You just walked into a hedge; you're stuck! Level Restarting....\n"
WINMESSAGE = "Congrats! "
TIMEDOUTMESSAGE = "You ran out of time! Level Restarting....\n"

#Colour Grid for easy reference
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

#States of direction
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

#Input name for highscores upon opening
playerName = str(raw_input("What is your name, it might appear on the highscores..."))

class mainGame:
    def __init__(self):
        return


def main():
    pygame.display.init()
    global FPSCLOCK, wn, BASICFONT
    pygame.init()
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
    time.sleep(5)
    loadlevel1(nofhedges)


def showStartScreen():
    global titleFont, instFont
    titleFont = pygame.font.SysFont('ActionIsShaded', 100)
    instFont = pygame.font.SysFont('ActionIsShaded', 25)
    titleSurf1 = titleFont.render('Hedge Maze', True, WHITE, RED)
    #Initial Starting Angles
    degrees1 = 0
##    print("Pre-loop show start screen: success")
    while True:
        wn.fill(BGCOLOR)
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        wn.blit(rotatedSurf1, rotatedRect1)
        levelDescr = instFont.render('Use the arrow keys to navigate your way to the golden square(watch out for the hedges)!', True, RED, WHITE)
        levelDescrRect = levelDescr.get_rect()
        levelDescrRect.center = (WINDOWWIDTH/2, WINDOWHEIGHT*0.10)
        wn.blit(levelDescr, levelDescrRect)
        drawPressKeyMsg()
        if checkForKeyPress():
            pygame.event.get()
            return
        pygame.display.update()
        degrees1 += 1
##        print("End of showstartscreen loop: success")
        time.sleep(0.02)
#Fake loading screen(to look professional)
def levelStartScreen():
    levelNameSurf1 = titleFont.render('LOADING', True, RED)
    levelNameRect1 = levelNameSurf1.get_rect()
    levelNameRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT * 0.25)
    levelDescr = instFont.render('You have ' + str(timer) +' seconds to complete each level.', True, BLUE)
    levelDescrRect = levelDescr.get_rect()
    levelDescrRect.center = (WINDOWWIDTH/2, WINDOWHEIGHT*0.75)
    wn.blit(levelDescr, levelDescrRect)
    wn.blit(levelNameSurf1, levelNameRect1)
    pygame.display.update()

def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press a key to play.', True, DARKGRAY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    wn.blit(pressKeySurf, pressKeyRect)

def terminate():
    #Ends all ongoing operations.
    end()
    pygame.quit()

def checkForKeyPress():
    #Key press log
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

#Highscore Display
def end():
    with open("Highscores.txt", "a") as myFile:
        myFile.write("\n"+str(playerName)+" Level "+str(level))
        #^Write command to a file


#Classes - Hedge, Player & Path

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

class pathTexture:

    def __init__(self):
        self.y = 0
        self.x = 0

    def loadTexture(self, x, y):
        self.texture = pygame.image.load("Path Texture.gif")
        self.texturerect = self.texture.get_rect()
        self.coords = (x, y)
        self.texturerect.move_ip(self.coords)
        wn.blit(self.texture, self.texturerect)
        pygame.display.flip()

class goalTexture:

    def __init__(self):
        self.y = 0
        self.x = 0

    def loadTexture(self):
        self.texture = pygame.image.load("Goal Texture.gif")
        self.texturerect = self.texture.get_rect()
        self.coords = (((WINDOWWIDTH/2)-CELLSIZE), ((WINDOWHEIGHT/2)-CELLSIZE))
        self.texturerect.move_ip(self.coords)
        wn.blit(self.texture, self.texturerect)
        pygame.display.flip()

#Level Create

def loadlevel1(nofhedges):
    global StartTime
    #Time log for time taken each level.
    StartTime = time.clock()
    count = 0
    hedges = 0
    global hedge1, hedgecoords, goalCoords, goal1
    clearScreen()
    drawGrid()
    player1 = playerTexture()
    player1.loadplayer(x, y)
    goals = 0
    goalCoords = []
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

#Fill Path Texture
##    for i in range(0, ((WINDOWHEIGHT/CELLSIZE) * (WINDOWWIDTH/CELLSIZE))):
##        pathx = 20
##        pathy = 20
##        pathCoords = (pathx, pathy)
##        path1 = pathTexture()
##        path1.loadTexture("hey", pathCoords)
##        while pathy<WINDOWHEIGHT:
##            while pathx<WINDOWWIDTH:
##                pathCoords = (pathx, pathy)
##                path1 = pathTexture()
##                path1.loadTexture("hola", pathCoords)
##                pathx+=20
##                if pathx==WINDOWWIDTH-CELLSIZE:
##                    pathx = 0
##                    pathy +=20
#Goal Comes Last

    while goals<1:
        goal1 = goalTexture()
        goal1.loadTexture()
        goals += 1
        goalCoords.insert(0, goal1.coords)
    while True:
        mainMove(x, y, nofhedges)

def mainMove(x, y, nofhedges):
    global level
    currentLives = 3
    direction = RIGHT
    fact = True
    while fact == True: # main game loop
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                currentTime = time.clock()
                #Key pressed moves on (waits until key is pressed to move on)
                #Logs
                if (event.key == K_LEFT or event.key == K_a):
                    direction = LEFT
                    levelCheck(level, fact)
                    locationDec(direction, x, y, currentLives, currentTime, nofhedges, level)

                elif (event.key == K_RIGHT or event.key == K_d):
                    direction = RIGHT
                    levelCheck(level, fact)
                    locationDec(direction, x, y, currentLives, currentTime, nofhedges, level)

                elif (event.key == K_UP or event.key == K_w):
                    direction = UP
                    levelCheck(level, fact)
                    locationDec(direction, x, y, currentLives, currentTime, nofhedges, level)

                elif (event.key == K_DOWN or event.key == K_s):
                    direction = DOWN
                    levelCheck(level, fact)
                    locationDec(direction, x, y, currentLives, currentTime, nofhedges, level)

                elif event.key == K_ESCAPE:
                    terminate()

        player1 = playerTexture()
        player1.loadplayer(x, y)

        if (x,y) in hedgecoords:
            currentLives-=1
            print(COLLISIONMESSAGE + str(currentLives) + " lives remaining.")
            time.sleep(2)
            loadlevel1(nofhedges)

##        elif (x,y) in goalCoords and (currentTime-StartTime)<timer and currentLives>0:
##            print(WINMESSAGE + "You took " + str(currentTime-StartTime)+" Seconds.")
##            time.sleep(3)
##            nofhedges+=50
##            level= level+1
##            loadlevel1(nofhedges)
##            print level
##            return level

def levelCheck(level,fact):
#Checks the level and fact is whether or not the five levels have been completed.
    if level>5:
        fact == False
        showStartScreen()
        runGame()
        return fact

def locationDec(direction, x, y, currentLives, currentTime, nofhedges, level):
    if (x,y) in goalCoords and (currentTime-StartTime)<timer and currentLives>0:
        print(WINMESSAGE + "You took " + str(currentTime-StartTime)+" Seconds.")
        time.sleep(3)
        nofhedges+=50
        level+=1
        loadlevel1(nofhedges)
        return level
        print level
    elif currentLives==0:
        terminate()
    elif (x,y) in goalCoords:
        currentLives-=1
        print(TIMEDOUTMESSAGE+ str(currentLives) + " lives remaining.")
        loadlevel1(nofhedges)
        currentLives-=1
    elif (x,y) in hedgecoords:
        currentLives-=1
        print(COLLISIONMESSAGE + str(currentLives) + " lives remaining.")
        time.sleep(2)
        loadlevel1(nofhedges)
    elif direction == RIGHT:
        if x<(WINDOWWIDTH-(2*CELLSIZE))+1:
            x+=CELLSIZE
            mainMove(x, y, nofhedges)
    elif direction == LEFT:
        if x>CELLSIZE-1:
            x-=CELLSIZE
            mainMove(x, y, nofhedges)
    elif direction == UP:
        if y>CELLSIZE-1:
            y-=CELLSIZE
            mainMove(x, y, nofhedges)
    elif direction == DOWN:
        if y<(WINDOWHEIGHT-(2*CELLSIZE))+1:
            y+=CELLSIZE
            mainMove(x, y, nofhedges)
    else:
        print("Out of play")
    return level
    print level

main()