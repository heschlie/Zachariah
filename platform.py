import pygame, sys
from pygame.locals import *


class Platform(pygame.sprite.Sprite):
    def __init__(self, loc, *groups):
        super(Platform, self).__init__(*groups)
        self.start = loc
        self.image = pygame.image.load('images/platform.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = self.start
        self.hitmask = pygame.mask.from_surface(self.image, 127)
        self.height_map = self.gen_height_map()
        self.type = 'solid'
        self.float_dist = 10
        self.speed = 0.15
        self.y_vel = 0
        self.max_speed = .25
        self.counter = 0
        
    def gen_height_map(self):
        test_mask = pygame.Mask((1, self.rect.height))
        test_mask.fill()
        heights = []
        mask = pygame.mask.from_surface(self.image, 127)
        for line in range(self.rect.width):
            height = mask.overlap_area(test_mask, (line, 0))
            heights.append(height)
        return heights
    
    def float(self, loc):
        if (self.rect.y - loc[1]) < (self.float_dist * -1):
            self.speed = 0.15
        if (self.rect.y - loc[1]) > self.float_dist:
            self.speed = -0.15
        self.y_vel += self.speed
        if abs(self.y_vel) > self.max_speed:
            if self.y_vel < 0:
                self.y_vel = self.max_speed * -1
            if self.y_vel > 0:
                self.y_vel = self.max_speed
        self.counter += self.y_vel        
        if abs(self.counter) >= 1:
            self.rect.y += self.counter
            self.counter = 0
                
    
    def update(self, dt, level, key):
        self.float(self.start)