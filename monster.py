import pygame, sys
from pygame.locals import *
from pixelperfect import *
from player import *
import tmx
import pyganim

class Monster(Character):
    def __init__(self, lvl, loc, *groups):
        super(Character, self).__init__(*groups)
        #self.sheet = pygame.image.load('images/enemy1a.png').convert_alpha()
        super(Monster, self).__init__(lvl, loc)
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
        if self.dir == left:
            self.x_vel -= self.speed
            self.image = self.animSurf['walk_left'].getCurrentFrame()
        if self.dir == right:
            self.x_vel += self.speed
            self.image = self.animSurf['walk_right'].getCurrentFrame()
        self.hitmask = pygame.mask.from_surface(self.image, 127)
        
        
class Walker(Monster):
    def __init__(self, lvl, loc, *groups):
        super(Character, self).__init__(*groups)
        self.sheet = pygame.image.load('images/enemy1a.png')
        super(Walker, self).__init__(lvl, loc)
        
    def get_images(self):
        self.face_right = self.sheet.subsurface((0,32,32,32))
        self.face_left = pygame.transform.flip(self.face_right, True, False)
        animSurf = {}
        imageAndDuration = [(self.sheet.subsurface((32*x,32,32,32)), 0.2) for x in range(4)]
        animSurf['walk_right'] = pyganim.PygAnimation(imageAndDuration)
        #flipping the right animations to create the left ones
        animSurf['walk_left'] = animSurf['walk_right'].getCopy()
        animSurf['walk_left'].flip(True, False)
        animSurf['walk_left'].makeTransformsPermanent()
        return animSurf
        
        
class Standing(Monster):
    def __init__(self, lvl, loc, *groups):
        super(Character, self).__init__(*groups)
        self.sheet = pygame.image.load('images/enemy1a.png')
        super(Standing, self).__init__(lvl, loc)
        self.speed = 0
        
    def get_images(self):
        self.face_right = self.sheet.subsurface((0,0,32,32))
        self.face_left = pygame.transform.flip(self.face_right, True, False)
        animSurf = {}
        imageAndDuration = [(self.sheet.subsurface((32*x,0,32,32)), 0.2) for x in range(4)]
        animSurf['walk_right'] = pyganim.PygAnimation(imageAndDuration)
        #flipping the right animations to create the left ones
        animSurf['walk_left'] = animSurf['walk_right'].getCopy()
        animSurf['walk_left'].flip(True, False)
        animSurf['walk_left'].makeTransformsPermanent()
        return animSurf