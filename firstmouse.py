import pygame
from pygame.locals import*

def get_clicked(mpos, row, wid, hei):
    counterx, countery = 0,0
    for item in range(row):
        if mpos[0] > (wid*item)-1:
            counterx += 1
        if mpos[1] > (hei*item)-1:
            countery +=1
    print mpos[1]
    print (counterx, countery)                    
    return (countery, counterx)
