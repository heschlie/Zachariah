import pygame, sys, player
from pygame.locals import *
from pixelperfect import *
import tmx
import os


def load():
    dt = 60
    
    pygame.init()
    screen = pygame.display.get_surface()
    
    clock = pygame.time.Clock()
    lvl = Level(screen, 'test')
    #for coord, cell in lvl.tilemap.layers['Tile Layer 1'].cells.items():
    #    print coord, cell.tile.gid
    #for i in lvl.height_dict:
    #    print i, lvl.height_dict[i]
    
    """Main loop"""
    while True:
        clock.tick(dt)
        
        lvl.tilemap.update(dt/1000., lvl)
        screen.fill((0,100,0))
        lvl.tilemap.draw(screen)
        #if lvl.tilemap.layers['Tile Layer 1'].get_at(lvl.hero.floor_detect_rects[0].x, lvl.hero.floor_detect_rects[0].bottom) != None:
            #print "test2 ", lvl.tilemap.layers['Tile Layer 1'].get_at(lvl.hero.rect.centerx, lvl.hero.rect.bottom).px, lvl.tilemap.layers['Tile Layer 1'].get_at(lvl.hero.rect.centerx, lvl.hero.rect.bottom).py
            #print "floor[0]", lvl.tilemap.layers['Tile Layer 1'].get_at(lvl.hero.floor_detect_rects[0].x, lvl.hero.floor_detect_rects[0].bottom).px, lvl.tilemap.layers['Tile Layer 1'].get_at(lvl.hero.floor_detect_rects[0].x, lvl.hero.floor_detect_rects[0].bottom).py
        #if lvl.tilemap.layers['Tile Layer 1'].get_at(lvl.hero.floor_detect_rects[1].x, lvl.hero.floor_detect_rects[1].bottom) != None:
            #print "floor[1]", lvl.tilemap.layers['Tile Layer 1'].get_at(lvl.hero.floor_detect_rects[1].x, lvl.hero.floor_detect_rects[1].bottom).px, lvl.tilemap.layers['Tile Layer 1'].get_at(lvl.hero.floor_detect_rects[1].x, lvl.hero.floor_detect_rects[1].bottom).py
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
                
class Level(object):
    
    def __init__(self, screen, name):
        
        os.chdir('levels/%s/' % name)
        self.level = "test.tmx"
        self.tilesheet = pygame.image.load('%s.png' % name)
        
        self.tilemap = tmx.load(self.level, screen.get_size())
        self.sprites = tmx.SpriteLayer()
        self.start_cell = self.tilemap.layers['triggers'].find('player')[0]
        os.chdir('../..')
        self.hero = player.Player(self, (self.start_cell.px, self.start_cell.py), self.sprites)
        self.rect_dict = self.tilemap.layers['Tile Layer 1'].cells
        self.height_dict = self.gen_height_map()
        
        
        self.tilemap.layers.append(self.sprites)
        
    def set_player_loc(self, player, loc):
        player.rect.center = loc
        
        
    def gen_height_map(self):
        height_dict = {}
        test_mask = pygame.Mask((1,self.tilemap.layers['Tile Layer 1'].tile_width))
        test_mask.fill()
        for coord, cell in self.rect_dict.items():
            heights = []
            mask = pygame.mask.from_surface(cell.tile.surface)
            for i in range(cell.tile.surface.get_width()):
                height = mask.overlap_area(test_mask,(i, 0))
                heights.append(height)
            height_dict[(coord)] = heights
        return height_dict
        
        
        
        
        