import pygame, sys, player
from pygame.locals import *
from pixelperfect import *
import tmx
import os


def load(world):
    dt = 60
    
    pygame.init()
    screen = pygame.display.get_surface()
    
    print world
    clock = pygame.time.Clock()
    lvl = Level(screen)
    
    while True:
        clock.tick(dt)
        
        lvl.tilemap.update(dt/1000., lvl)
        screen.fill((0,100,0))
        lvl.tilemap.draw(screen)
        print lvl.tilemap.layers['Tile Layer 1'].get_at(lvl.hero.rect.centerx, lvl.hero.rect.centery)
        print lvl.hero.rect.centerx, lvl.hero.rect.centery
        
        #screen.blit(lvl.lvl_bg, lvl.rect)
        #screen.blit(hero.image, hero.rect)
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
                
class Level(object):
    
    def __init__(self, screen):
        
        dt = 60

        #self.lvl_bg, self.rect = load_image('test_level.png', None, True)
        #self.hitmask = pygame.surfarray.array_alpha(self.lvl_bg)
        
        self.level = "levels/test/untitled.tmx"
        
        self.tilemap = tmx.load(self.level, screen.get_size())
        self.sprites = tmx.SpriteLayer()
        self.start_cell = self.tilemap.layers['triggers'].find('player')[0]
        
        self.hero = player.Player(self, (self.start_cell.px, self.start_cell.py), self.sprites)
        
        
        self.tilemap.layers.append(self.sprites)
        
    def set_player_loc(self, player, loc):
        player.rect.center = loc
        
        