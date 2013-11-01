#!/usr/bin/python

import pygame, sys
from pygame.locals import *
import level, settings

pygame.init()

def mainMenu():
    global RES, DISPSURF, mouseClick
    # Trying to make the menu/game multiresolution capable, might not pan out
    RES = [(1280,720), (1920,1080)]
    resolution = 0
    DISPSURF = pygame.display.set_mode(RES[resolution])
    
    mouseClick = False
    mousex = 0
    mousey = 0
    
    pygame.display.set_caption("Zacharaiah")
    
    while True:
        mouseClick = False
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClick = True
        
        #lvl = level.Level(DISPSURF)
        menuFont = pygame.font.Font('freesansbold.ttf', 32)
        #buttonFont = pygame.font.Font('freesansbold.ttf', 24)
        playImg = pygame.image.load('images/play.png').convert()
        settingsImg = pygame.image.load('images/settings.png').convert()
        playHover = pygame.image.load('images/playHover.png').convert()
        settingsHover = pygame.image.load('images/settingsHover.png').convert()
        
        title = menuFont.render('Zacharaiah', True, (0,0,0))
        titleObj = title.get_rect()
        titleObj.center = (1280 * .5), (720 * .1)
        
        #Draw button images using a small amount of math to hold position over resolution changes
        DISPSURF.blit(playImg,(1280 * .175,720 * .417))
        DISPSURF.blit(settingsImg,(1280 * .511,720 * .417))
        
        #Setup button hover image swap
        hovA = DISPSURF.blit(playImg,(1280 * .175,720 * .417))
        hovB = DISPSURF.blit(settingsImg,(1280 * .511,720 * .417))
        if hovA.collidepoint(pygame.mouse.get_pos()):
            DISPSURF.blit(playHover,(1280 * .175,720 * .417))
        if hovB.collidepoint(pygame.mouse.get_pos()):
            DISPSURF.blit(settingsHover,(1280 * .511,720 * .417))
        
        #Load the overworld upon clicking 'Play' button    
        if hovA.collidepoint(pygame.mouse.get_pos()) and mouseClick == True:
            level.load('foo')
    
        if hovB.collidepoint(pygame.mouse.get_pos()) and mouseClick == True:
            settings.settingsMenu('bar')
            
            
        pygame.draw.rect(DISPSURF, (0,255,0), (((1280 - 200) * .5), (720 * .1) - 25, 200, 50))
        
        DISPSURF.blit(title, titleObj)
        pygame.display.update()

if __name__ == "__main__":
    mainMenu()