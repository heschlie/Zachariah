import pygame, sys
from pygame.locals import *
from character import *

class Monster(Character):
    def __init__(self, lvl, loc, *groups):
        super(Character, self).__init__(*groups)
        self.image = self.animSurf['idle_left'].getCurrentFrame()
        super(Monster, self).__init__(lvl, loc)
        self.dir = 'left'
        self.start = loc
        self.rect.center = self.start
        self.speed = 2
        self.patrol_distance = 160
        
    def update(self, dt, lvl, key):
        super(Monster, self).update(dt, lvl, key)
        self.move()
        
    def move(self):
        self.conductor.play()
        self.x_vel = 0
        right = 'right'
        left = 'left'
        if abs(self.rect.left - self.start[0]) > self.patrol_distance:
            self.dir = right
        if abs(self.rect.right - self.start[0]) > self.patrol_distance:
            self.dir = left
        #setting directions for idle
        if self.dir == 'left':
            self.image = self.animSurf['idle_left'].getCurrentFrame()
            self.hitmask = self.hitmask_dict['idle_left'][self.animSurf['idle_left']._propGetCurrentFrameNum()]
        if self.dir == 'right':
            self.image = self.animSurf['idle_right'].getCurrentFrame()
            self.hitmask = self.hitmask_dict['idle_right'][self.animSurf['idle_right']._propGetCurrentFrameNum()]
        if self.dir == left and self.speed > 0:
            self.image = self.animSurf['walk_left'].getCurrentFrame()
            self.hitmask = self.hitmask_dict['walk_left'][self.animSurf['walk_left']._propGetCurrentFrameNum()]
            self.x_vel -= self.speed
        if self.dir == right and self.speed > 0:
            self.image = self.animSurf['walk_right'].getCurrentFrame()
            self.hitmask = self.hitmask_dict['walk_right'][self.animSurf['walk_right']._propGetCurrentFrameNum()]
            self.x_vel += self.speed
        
        
class Walker(Monster):
    def __init__(self, lvl, loc, *groups):
        super(Character, self).__init__(*groups)
        self.sheet = pygame.image.load('images/enemy1a.png').convert_alpha()
        self.animTypes = 'idle_right walk_right run_right'.split()
        self.placeholder = self.sheet.subsurface(0, 0, 32, 32)
        self.animSurf, self.hitmask_dict = self.get_images(self.sheet, self.animTypes, 32, 32)
        super(Walker, self).__init__(lvl, loc)

class Standing(Monster):
    def __init__(self, lvl, loc, *groups):
        super(Character, self).__init__(*groups)
        self.sheet = pygame.image.load('images/enemy1a.png').convert_alpha()
        self.animTypes = 'idle_right walk_right run_right'.split()
        self.placeholder = self.sheet.subsurface(0, 0, 32, 32)
        self.animSurf, self.hitmask_dict = self.get_images(self.sheet, self.animTypes, 32, 32)
        super(Standing, self).__init__(lvl, loc)
        self.speed = 0