import pygame, sys, player
from pygame.locals import *
from pixelperfect import *
#from main import *

def load(world):
    pygame.init()
    screen = pygame.display.get_surface()
    
    print world
    clock = pygame.time.Clock()
    lvl = Level()
    hero = player.Player()
    
    lvl.set_player_loc(hero, 100,100)
    
    while True:
        dt = 60
        clock.tick(dt)
        
        hero.update(dt/1000., lvl)
        
        screen.fill((0,100,0))
        screen.blit(lvl.lvl_bg, lvl.rect)
        screen.blit(hero.image, hero.rect)
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

class Level(object):
    
    def __init__(self,):

        self.lvl_bg, self.rect = load_image('test_level.png', None, True)
        self.hitmask = pygame.surfarray.array_alpha(self.lvl_bg)
        
    def set_player_loc(self, player, x, y):
        player.rect.center = (x, y)