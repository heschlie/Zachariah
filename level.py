import pygame
import player
import platform
import monster
import sys
from pygame.locals import *
import tmx
import os


def load():
    dt = 60.0
    
    pygame.init()
    screen = pygame.display.get_surface()
    
    clock = pygame.time.Clock()
    lvl = Level(screen, 'beta')

    joysticks = []
    for i in range(0, pygame.joystick.get_count()):
        joysticks.append(pygame.joystick.Joystick(i))
        joysticks[-1].init()

    #Main Loop
    while True:
    #     if lvl.hero.dead:
    #        break
        keys = pygame.event.get()
        for event in keys:
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    lvl.hero.jump()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    lvl.hero.jump_cut()
            elif event.type == JOYBUTTONDOWN:
                if event.button == 0:
                    lvl.hero.jump()
            elif event.type == JOYBUTTONUP:
                if event.button == 0:
                    lvl.hero.jump_cut()

        key = pygame.key.get_pressed()
        lvl.tilemap.update(dt, lvl, key, joysticks, screen)
        screen.fill((0, 100, 0))
        lvl.tilemap.draw(screen)
        pygame.display.set_caption("{} - FPS: {:.2f}".format("Zachariah", clock.get_fps()))

        pygame.display.update()
        clock.tick(dt)


class Level(object):
    def __init__(self, screen, name):
        """Loading the level files, changing the CWD to match the files for loading,
        This was easier than having to edit the .tmx file every time it needed to
        be edited."""
        os.chdir('levels/%s/' % name)
        self.level = "%s.tmx" % name
        self.tilemap = tmx.load(self.level, screen.get_size())
        os.chdir('../..')

        #Loading platforms, this needs to come before the player so the player is drawn on top
        #of the platform sprites, and so he will move with the platforms
        self.platforms = tmx.SpriteLayer()
        for plat in self.tilemap.layers['platforms'].find('platform'):
            platform.Platform((plat.px, plat.py), self.platforms)
        self.tilemap.layers.append(self.platforms)        
        
        #Loading the 'hero' into the level, and adding him/her to the self.sprites group
        self.sprites = tmx.SpriteLayer()
        self.start_cell = self.tilemap.layers['spawns'].find('player')[0]
        self.hero = player.Player(self, (self.start_cell.px, self.start_cell.py), self.sprites)
        #self.hero_ear = player.Ears(self, (self.start_cell.px, self.start_cell.py), self.sprites)
        self.tilemap.layers.append(self.sprites)
        
        #Cell, rect, and mask dicts
        self.cell_size = (self.tilemap.layers['terrain'].tile_width, self.tilemap.layers['terrain'].tile_height)
        self.cells_dict = self.tilemap.layers['terrain'].cells
        self.height_dict = self.gen_height_map()
        self.rect_dict = self.get_rect_dict()
        self.mask_dict = self.make_mask_dict()

        #Load the monsters.  Set the value of the enemy property to the class you wish to make a monster from
        self.enemies = tmx.SpriteLayer()
        for enemy in self.tilemap.layers['spawns'].find('enemy'):
            if enemy.properties['enemy'] == 'walker':
                monster.Walker(self, (enemy.px, enemy.py), self.enemies)
            if enemy.properties['enemy'] == 'standing':
                monster.Standing(self, (enemy.px, enemy.py), self.enemies)
        self.tilemap.layers.append(self.enemies)
        
        #for test in self.enemies.__iter__():
        #    print test.rect
        
    def get_rect_dict(self):
        rect_dict = {}
        for coord, cell in self.cells_dict.items():
            rect_dict[coord] = cell.tile.surface.get_rect(x=coord[0] * self.cell_size[0],
                                                          y=coord[1] * self.cell_size[1])
        return rect_dict

    def gen_height_map(self):
        height_dict = {}
        test_mask = pygame.Mask((1, self.tilemap.layers['terrain'].tile_height))
        test_mask.fill()
        for coord, cell in self.cells_dict.items():
            heights = []
            mask = pygame.mask.from_surface(cell.tile.surface)
            for i in range(cell.tile.surface.get_width()):
                height = mask.overlap_area(test_mask, (i, 0))
                heights.append(height)
            height_dict[coord] = heights
        return height_dict
    
    def make_mask_dict(self):
        mask_dict = {}
        for i, cell in self.cells_dict.items():
            mask_dict[i] = pygame.mask.from_surface(cell.tile.surface)
        return mask_dict