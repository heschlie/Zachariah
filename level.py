import pygame
import player
import platform
import monster
import npc
import parallax
import dict_dump
import sys
from pygame.locals import *
import tmx
import os


def load():
    dt = 60.0
    
    pygame.init()
    screen = pygame.display.get_surface()

    monsters = dict_dump.monsters
    friendies = dict_dump.npc
    lvl_dict = dict_dump.levels
    
    clock = pygame.time.Clock()
    lvl = Level(screen, lvl_dict['test'], monsters, friendies)

    joysticks = []
    for i in range(0, pygame.joystick.get_count()):
        joysticks.append(pygame.joystick.Joystick(i))
        joysticks[-1].init()

    #Main Loop
    while True:
        if lvl.hero.dead:
            break
        keys = pygame.event.get()
        for event in keys:
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

        key = pygame.key.get_pressed()
        lvl.tilemap.update(dt, lvl, key, joysticks, screen, keys)
        lvl.parallax.update(dt, lvl, key, joysticks, screen, keys)
        screen.fill(lvl.bg_color)

        for key in sorted(lvl.para_layers_dict.keys()):
            para = lvl.para_layers_dict[key]
            para.para_blit(screen, lvl)

        lvl.tilemap.draw(screen)
        lvl.tilemap.layers['foreground'].draw(screen)

        pygame.display.set_caption("{} - FPS: {:.2f}".format("Zachariah", clock.get_fps()))
        pygame.display.update()
        clock.tick(dt)


class Level(object):
    def __init__(self, screen, lvl_dict, monsters, friendlies):
        """Loading the level files, changing the CWD to match the files for loading,
        This was easier than having to edit the .tmx file every time it needed to
        be edited."""
        self.bg_color = lvl_dict['bg_color']
        name = lvl_dict['name']
        para_layers = lvl_dict['para']
        para_speed = lvl_dict['para_speed']
        para_start = lvl_dict['para_start']

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

        #Load in NPCs
        self.npc = tmx.SpriteLayer()
        for npcs in self.tilemap.layers['spawns'].find('npc'):
            friendlies[npcs.properties['npc']](self, (npcs.px, npcs.py), npcs.properties, self.npc)
        self.tilemap.layers.append(self.npc)
        
        #Loading the 'hero' into the level, and adding him/her to the self.sprites group
        self.sprites = tmx.SpriteLayer()
        self.start_cell = self.tilemap.layers['spawns'].find('player')[0]
        hero_spawn = self.tilemap.layers['spawns'].find('player')[0]
        self.hero = player.Player(self, (self.start_cell.px, self.start_cell.py), hero_spawn.properties, self.sprites)
        self.tilemap.layers.append(self.sprites)
        
        #Cell, rect, and mask dicts
        self.cell_size = (self.tilemap.layers['terrain'].tile_width, self.tilemap.layers['terrain'].tile_height)
        self.cells_dict = self.tilemap.layers['terrain'].cells
        self.height_dict = self.gen_height_map(self.cells_dict)
        self.rect_dict = self.get_rect_dict(self.cells_dict)
        self.mask_dict = self.make_mask_dict(self.cells_dict)

        #Same for the terrain-bg layer
        self.cell_bg_dict = self.tilemap.layers['terrain_bg'].cells
        self.bg_height_dict = self.gen_height_map(self.cell_bg_dict)
        self.bg_rect_dict = self.get_rect_dict(self.cell_bg_dict)
        self.bg_mask_dict = self.make_mask_dict(self.cell_bg_dict)

        #Load the monsters.  Set the value of the enemy property to the class you wish to make a monster from
        self.enemies = tmx.SpriteLayer()
        for enemy in self.tilemap.layers['spawns'].find('enemy'):
            monsters[enemy.properties['enemy']](self, (enemy.px, enemy.py), enemy.properties, self.enemies)
        self.tilemap.layers.append(self.enemies)

        #Loading the parallaxed background layers
        self.para_layers_dict = {}
        self.parallax = pygame.sprite.Group()
        for i, para in para_layers.items():
            parallax.ParaLayer(para, para_start[i], para_speed[i], i, lvl_dict['para_offset'], self.parallax)
        for para in self.parallax:
            self.para_layers_dict[para.name] = para

    def get_rect_dict(self, cells_dict):
        rect_dict = {}
        for coord, cell in cells_dict.items():
            rect_dict[coord] = cell.tile.surface.get_rect(x=coord[0] * self.cell_size[0],
                                                          y=coord[1] * self.cell_size[1])
        return rect_dict

    def gen_height_map(self, cells_dict):
        height_dict = {}
        test_mask = pygame.Mask((1, self.tilemap.layers['terrain'].tile_height))
        test_mask.fill()
        for coord, cell in cells_dict.items():
            heights = []
            mask = pygame.mask.from_surface(cell.tile.surface)
            for i in range(cell.tile.surface.get_width()):
                height = mask.overlap_area(test_mask, (i, 0))
                heights.append(height)
            height_dict[coord] = heights
        return height_dict
    
    def make_mask_dict(self, cells_dict):
        mask_dict = {}
        for i, cell in cells_dict.items():
            mask_dict[i] = pygame.mask.from_surface(cell.tile.surface)
        return mask_dict