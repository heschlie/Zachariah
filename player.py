import pygame, sys
from character import *
from pygame.locals import *


class Player(Character):
    def __init__(self, lvl, loc, *groups):
        super(Character, self).__init__(*groups)
        self.sheet = pygame.image.load('images/char.png').convert_alpha()
        animTypes = 'idle_right walk_right run_right jump_right fall_right tred_right swim_right stop_right ' \
                    'damage_right'.split()
        self.placeholder = self.sheet.subsurface(0, 0, 32, 64)
        self.animSurf, self.hitmask_dict = self.get_images(self.sheet, animTypes, 32, 64)
        self.image = self.animSurf['idle_right'].getCurrentFrame()
        super(Player, self).__init__(lvl, loc)
        self.rect.center = loc
        
    def update(self, dt, lvl, key):
        self.check_keys(key)
        super(Player, self).update(dt, lvl, key)
        lvl.tilemap.set_focus(self.rect.centerx, self.rect.centery)
        self.speed = 3
        
    def check_keys(self, key):
        self.x_vel = 0
        #setting directions for idle
        if self.dir == 'left':
            self.image = self.animSurf['idle_left'].getCurrentFrame()
            self.hitmask = self.hitmask_dict['idle_left'][self.animSurf['idle_left']._propGetCurrentFrameNum()]
        if self.dir == 'right':
            self.image = self.animSurf['idle_right'].getCurrentFrame()
            self.hitmask = self.hitmask_dict['idle_right'][self.animSurf['idle_right']._propGetCurrentFrameNum()]
        if key[pygame.K_LSHIFT]:
            self.speed = 6
        if key[pygame.K_LEFT]:
            if self.speed == 3:
                self.image = self.animSurf['walk_left'].getCurrentFrame()
                self.hitmask = self.hitmask_dict['walk_left'][self.animSurf['walk_left']._propGetCurrentFrameNum()]
            if self.speed == 6:
                self.image = self.animSurf['run_left'].getCurrentFrame()
                self.hitmask = self.hitmask_dict['run_left'][self.animSurf['run_left']._propGetCurrentFrameNum()]
            self.dir = 'left'
            self.x_vel -= self.speed
        if key[pygame.K_RIGHT]:
            if self.speed == 3:
                self.image = self.animSurf['walk_right'].getCurrentFrame()
                self.hitmask = self.hitmask_dict['walk_right'][self.animSurf['walk_right']._propGetCurrentFrameNum()]
            if self.speed == 6:
                self.image = self.animSurf['run_right'].getCurrentFrame()
                self.hitmask = self.hitmask_dict['run_right'][self.animSurf['run_right']._propGetCurrentFrameNum()]
            self.dir = 'right'
            self.x_vel += self.speed