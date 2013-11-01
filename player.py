import pygame, sys
from pygame.locals import *
from pixelperfect import *

class Player(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super(Player, self).__init__(*groups)
        
        self.image, self.rect = load_image('images/player.png', None, True)
        #self.hitmask = get_alpha_hitmask(self.image, self.rect, 255)
        self.hitmask = pygame.surfarray.array_alpha(self.image)
        self.resting = False
        self.dy = 0
        self.speed = 50
        
    def update(self, dt, lvl):
        #last = self.rect.copy()

        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.rect.x -= self.speed * dt
        if key[pygame.K_RIGHT]:
            self.rect.x += self.speed * dt
        if key[pygame.K_DOWN]:
            self.rect.y += self.speed * dt
        if key[pygame.K_UP]:
            self.rect.y -= self.speed * dt
        if self.resting and key[pygame.K_SPACE]:
            self.dy = -500
        #self.dy = min(400, self.dy + 40)
        self.rect.y += self.dy * dt
        
        
        if check_collision(lvl, self):
            print "Colliding"
            