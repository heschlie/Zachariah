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
        self.float_dist_y = 10
        self.float_dist_x = 100
        self.speed = 0.15
        self.y_vel = 0
        self.x_vel = 0
        self.max_speed = 1
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
        if (self.rect.y - loc[1]) < (self.float_dist_y * -1):
            self.speed = 0.15
        if (self.rect.y - loc[1]) > self.float_dist_y:
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

    def move(self, loc):
        if (self.rect.x - loc[0]) < (self.float_dist_x * -1):
            self.speed = 0.15
        if (self.rect.x - loc[0]) > self.float_dist_x:
            self.speed = -0.15
        self.x_vel += self.speed
        if abs(self.x_vel) > self.max_speed:
            if self.x_vel < 0:
                self.x_vel = self.max_speed * -1
            if self.x_vel > 0:
                self.x_vel = self.max_speed
        self.rect.x += self.x_vel

    def adjust_character_speed(self, level):
        x_vel = int(self.x_vel)
        y_vel = int(self.y_vel)
        test = pygame.Rect((self.rect.x - x_vel, self.rect.y - y_vel), self.rect.size)
        for mob in level.enemies:
            mask_test = test.x - mob.rect.x, test.y - mob.rect.y
            if mob.hitmask.overlap(self.hitmask, mask_test):
                mob.plat_speed = self.x_vel
        for sprite in level.sprites:
            mask_test = test.x - sprite.rect.x, test.y - sprite.rect.y - 10
            if sprite.hitmask.overlap(self.hitmask, mask_test):
                sprite.rect.x += self.x_vel

    def update(self, dt, level, key):
        #self.float(self.start)
        self.move(self.start)
        self.adjust_character_speed(level)