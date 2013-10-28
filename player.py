import pygame, sys
from pygame.locals import *
from pixelperfect import *

class Player(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super(Player, self).__init__(*groups)
        
        self.image, self.rect = load_image('images/player.png', None, True)
        self.hitmask = get_alpha_hitmask(self.image, self.rect, 127)