#!/usr/bin/python3

import pygame, sys
from pygame.locals import *
import level, settings

pygame.init()


def main():
    # Trying to make the menu/game multiresolution capable, might not pan out
    res = [(1280, 720), (1920, 1080)]
    resolution = 0
    screen = pygame.display.set_mode(res[resolution])
    
    pygame.display.set_caption("Zacharaiah")
    play_btn = Button('images/play.png', 'images/playHover.png', (1280 * .175, 720 * .417))
    settings_btn = Button('images/settings.png', 'images/settingsHover.png', (1280 * .511, 720 * .417))
    
    while True:
        mouseClick = False
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                mouseClick = True

        screen.fill((0, 0, 0))
        menuFont = pygame.font.Font('freesansbold.ttf', 32)
        
        title = menuFont.render('Zacharaiah', True, (0, 0, 0))
        titleObj = title.get_rect()
        titleObj.center = (1280 * .5), (720 * .1)

        play_btn.reset_img()
        settings_btn.reset_img()
        if play_btn.rect.collidepoint(pygame.mouse.get_pos()):
            play_btn.img_hover()
        if settings_btn.rect.collidepoint(pygame.mouse.get_pos()):
            settings_btn.img_hover()
        
        #Load the overworld upon clicking 'Play' button    
        if play_btn.rect.collidepoint(pygame.mouse.get_pos()) and mouseClick:
            level.load()
    
        if settings_btn.rect.collidepoint(pygame.mouse.get_pos()) and mouseClick:
            settings.settingsMenu('bar')

        pygame.draw.rect(screen, (0, 255, 0), (((1280 - 200) * .5), (720 * .1) - 25, 200, 50))
        
        screen.blit(title, titleObj)
        screen.blit(play_btn.image, play_btn.rect)
        screen.blit(settings_btn.image, settings_btn.rect)
        pygame.display.update()


class Button(object):
    def __init__(self, img1, img2, loc):
        self.image = pygame.image.load(img1).convert()
        self.def_image = self.image
        self.hover = pygame.image.load(img2).convert()
        self.rect = self.image.get_rect()
        self.rect.topleft = loc

    def img_hover(self):
        self.image = self.hover

    def reset_img(self):
        self.image = self.def_image


if __name__ == "__main__":
    main()