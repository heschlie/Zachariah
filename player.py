import pygame, sys
from pygame.locals import *
from pixelperfect import *
import tiledtmxloader

class Player(pygame.sprite.Sprite):
    def __init__(self):
        #super(Player, self).__init__(*groups)
        
        self.image, self.rect = load_image('images/player.png', None, True)
        self.hitmask = pygame.surfarray.array_alpha(self.image)
        self.resting = False
        self.dy = 0
        self.speed = 50
        self.flrA = Detectors(self.rect.x+1, self.rect.y, 1,self.rect.height+16)
        self.flrB = Detectors(self.rect.right-2, self.rect.y, 1,self.rect.height+16)
        self.wall = Detectors(self.rect.x, self.rect.bottom-30, self.rect.width, 1)
        self._sprite = tiledtmxloader.helperspygame.SpriteLayer.Sprite(self.image, self.rect)
        self.herox = 100
        self.heroy = 100
        
    def update(self, dt, lvl):
        last = self.rect.copy()

        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            #self._sprite.rect.centerx -= self.speed * dt
            self.herox -= self.speed * dt
        if key[pygame.K_RIGHT]:
            #self._sprite.rect.centerx += self.speed * dt
            self.herox += self.speed * dt
        if key[pygame.K_DOWN]:
            #self._sprite.rect.centery += self.speed * dt
            self.heroy += self.speed * dt
        if key[pygame.K_UP]:
            #self._sprite.rect.centery -= self.speed * dt
            self.heroy -= self.speed * dt
        if self.resting and key[pygame.K_SPACE]:
            self.dy = -200
        #self.dy = min(400, self.dy + 20)
        self.rect.y += self.dy * dt
        self.rect.centerx = self.herox
        self.rect.centery = self.heroy
        
        
        if check_collision(self.flrA, lvl):
            print "Collision detected"
            
class Detectors(object):
    def __init__(self, x, y, width, height):
        self.image = pygame.Rect((x, y),(width, height))
        #self.hitmask = pygame.Mask.self.image