import pygame, sys, player
from pygame.locals import *
from pixelperfect import *
from main import *

def load(world, screen):
    pygame.init()
    screen = screen
    
    print world
    clock = pygame.time.Clock()
    hero = player.Player(screen)
    lvl = Level(screen)
    
    while True:
        clock.tick(60)
        
        screen.fill((0,100,0))
        screen.blit(lvl.lvl_bg, lvl.rect)
        screen.blit(hero.image, hero.rect)
        pygame.display.update()

class Level(object):
    
    #lvl_bg = pygame.image.load('test_level.png')
    #lvl_bg = lvl_bg.convert_alpha()
    #rect = lvl_bg.get_rect()
    lvl_bg, rect = load_image('test_level.png', None, True)
    hitmask = get_alpha_hitmask(lvl_bg, rect, 127)
    
    def __init__(self, screen):
        self.screen = screen
        
        #lvl_img = pygame.image.load('test_level.png')
        #self.lvl_bg, self.rect = load_image('test_level.png', None, True)
        #self.hitmask = get_alpha_hitmask(self.lvl_bg, self.rect, 127)