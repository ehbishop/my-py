
import pygame
import sys
from pygame.locals import *
import random
import firstmouse

pygame.init
#Can this be made user adjustable?
reso = (640, 360)
windowSurfaceObj = pygame.display.set_mode(reso)

fpsClock = pygame.time.Clock()
pygame.display.set_caption('SquareLock')

Red = pygame.Color(255, 0, 0)
Blue = pygame.Color(0, 0, 255)
hues = (True, False)


class Gameset:
    def __init__(self, reso=reso):
        self.row = input('How many rows?')
        self.widbox = {}
        self.heibox = {}
        self.wid = (float(reso[0])/self.row)
        self.hei = (float(reso[1])/self.row)
        self.sections = {}
        self.stati = {}
        self.gfx = {}

    def grid(self):
        counter = 1
        for item in range(0, self.row):
            #e.g. hei*0 = 0, so first rect will start at 0 px
            self.widbox[item+1] = item*self.wid
            self.heibox[item+1] = item*self.hei
        for item in self.heibox:
            for item2 in self.widbox:
                self.sections[counter] = (item,item2)
                #rect coordinates
                #As above, starts at width/height 0 and extends to 
                #the width of the rects.  E.g: rect of area Z:wi placed at
                #coordinate (x,y)
                self.gfx[self.sections[counter]] = (self.widbox[item2], 
                        self.heibox[item], self.wid - 2, self.hei - 2)
                counter += 1

#edit to include input, levels
    def boardstate(self, lvl = 0):
        bsg = []
        if lvl == 0:
            for item in self.sections:
                bsg+= [random.choice(hues)]
        return bsg

    def gen_status(self, lvl = 0):
        self.grid()
        bsg = self.boardstate(lvl)
        for item in self.sections:
            self.stati[self.sections[item]] = bsg[item-1]
        
    def newgame(self, lvl = 0):
        self.gen_status(lvl)
        self.update_game(self.sections)
        
    def game_end(self):
        pass 

    def plays(self, (s1, s2)):
        effects = {}
        effects[1] = self.section1 = (s1, s2)
        effects[2] = self.section2 = (s1-1, s2)
        effects[3] = self.section3 = (s1, s2-1)
        effects[4] = self.section4 = (s1+1, s2)
        effects[5] = self.section5 = (s1, s2+1)
        for item in effects:
            if self.stati.has_key(effects[item]) == True:
                self.stati[effects[item]] = not(self.stati[effects[item]])
        self.update_game(effects)

    def update_game(self, changes = {}):
        for item in changes:
            if self.gfx.has_key(changes[item]) and self.stati.has_key(
                                                        changes[item]):
                onJect(self.gfx[changes[item]],self.stati[changes[item]
                                                                ]).place()
                pygame.display.update()


class onJect:
    #Creates a Square for the designated space on board
    def __init__(self, coordinates, status = False):
        self.status = status
        if self.status:
            self.color = Blue
        else:
            self.color = Red
        self.LOC = coordinates
    
    def place(self):
        pygame.draw.rect(windowSurfaceObj, self.color, self.LOC)


def Selection(controller):
    x = input('1 - %s please' % (row*row))
    x = controller[x]
    return x


lightboard = Gameset()
lightboard.newgame()

while 1:
    running = True
    while running == True:
    ##Win Condition State check
        x = 0
        for item in lightboard.stati:
            if lightboard.stati[item] == False:
                x = 1
        if x == 0:
            break
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0] == 1:
                    mpos = pygame.mouse.get_pos()
                    lightboard.plays(firstmouse.get_clicked(
                                                            mpos,lightboard.row,
                                                            lightboard.wid, 
                                                            lightboard.hei))
        if event.type == pygame.QUIT:
            running = False
        # lightboard.plays(Selection(lightboard.sections))

    ng = raw_input('New game?')
    if ng[0].lower() == 'y':
        windowSurfaceObj.fill((0,0,0))
        lightboard = Gameset()
        lightboard.newgame()
    else:
        break

pygame.time.wait(100)
        
#Observations:  The levels load would supercede the input of rows.
#This will make for more efficient code.
#Still needs to be tidier, but, on the whole, this is way more efficient.
#Choices made to create game in OO format will enable efficient gamestate
#'saving' as easier addition to make in the future.
#Obviously the exit loop needs to be changed
#put row input in "new game".  
#integrate rects for better control
    
    

