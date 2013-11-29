import pygame, sys
from pygame.locals import *
from pixelperfect import *
import tmx
import pyganim

class Platform(pygame.sprite.Sprite):
    def __init__(self, loc, *groups):
        super(Platform, self).__init__(*groups)
        self.image = pygame.image.load('images/platform.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = loc
        self.hitmask = pygame.surfarray.array_alpha(self.image)
        self.height_map = self.gen_height_map()
        
        
    def gen_height_map(self):
        test_mask = pygame.Mask((1, self.rect.height))
        test_mask.fill()
        heights = []
        mask = pygame.mask.from_surface(self.image, 127)
        for line in self.rect.width:
            height = mask.overlap_area(test_mask, (line, 0))
            heights.append(height)
        return heights
            