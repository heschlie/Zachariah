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