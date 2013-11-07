import pygame, sys
from pygame.locals import *
from pixelperfect import *
import tmx
class Character(pygame.sprite.Sprite):
    def __init__(self):
        self.test123 = "abc"
        
        
class Player(Character):
    def __init__(self, lvl, loc, *groups):
        super(Character, self).__init__(*groups)
        
        self.image, self.rect = load_image('images/player.png', None, True)
        self.hitmask = pygame.surfarray.array_alpha(self.image)
        self.reset_wall_floor_rects()
        self.fall = False
        self.dy = 0
        self.speed = 50
        lvl.set_player_loc(self, (loc))
        
    def update(self, dt, lvl):
        last = self.rect.copy()

        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.rect.centerx -= self.speed * dt
            #self.herox -= self.speed * dt
        if key[pygame.K_RIGHT]:
            self.rect.centerx += self.speed * dt
            #self.herox += self.speed * dt
        if key[pygame.K_DOWN]:
            self.rect.centery += self.speed * dt
            #self.heroy += self.speed * dt
        if key[pygame.K_UP]:
            self.rect.centery -= self.speed * dt
            #self.heroy -= self.speed * dt
        if not self.fall and key[pygame.K_SPACE]:
            self.dy = -200
        #self.dy = min(400, self.dy + 20)
        self.rect.y += self.dy * dt
        
        self.detect_ground(lvl)
        self.reset_wall_floor_rects()
        
        lvl.tilemap.set_focus(self.rect.centerx, self.rect.centery)
        
    def detect_ground(self, level):
        if not self.fall:
            self.grounded(level)
        self.reset_wall_floor_rects()
              
    def grounded(self, level):
        change = None
        pads_on = [False, False]
        for i, floor in enumerate(self.floor_detect_rects):
            collide, pads_on = self.check_floor_initial(pads_on, (i, floor), level)
            if collide:
                change = self.check_floor_final(collide, (i, floor), change, level)
        if change != None:
            self.rect.y = int(change - self.rect.height)
        #else:
            #self.fall = True
                     
                     
    def check_floor_initial(self, pads_on, pad_details, level):
        i, floor = pad_details
        collide = []
        for cell in level.rect_dict:
            if floor.colliderect(level.rect_dict[cell].tile.surface.get_bounding_rect()):
                collide.append(cell) 
                pads_on[i] = True
        print collide        
        return collide, pads_on
         
         
    def check_floor_final(self, collide, pad_details, change, level):
        i, floor = pad_details
        for key in collide:
            cell_heights = level.height_dict[key]
            x_in_cell = floor.x - key[0] * level.tilemap.layers['Tile Layer 1'].tile_width
            print x_in_cell
            offset = cell_heights[x_in_cell]
            
            if change == None:
                change = (key[1] + 1) * level.tilemap.layers['Tile Layer 1'].tile_width - offset
            else:
                change = min((key[1] + 1) * level.tilemap.layers['Tile Layer 1'].tile_width - offset, change)
        return change
      
      
    def reset_wall_floor_rects(self):
        flr = (pygame.Rect((self.rect.x+1,self.rect.y),(1,self.rect.height+16)),
               pygame.Rect((self.rect.right-2,self.rect.y),(1,self.rect.height+16)))
        wall = pygame.Rect(self.rect.x,self.rect.bottom-10,self.rect.width,1)
        self.floor_detect_rects = flr
        self.wall_detect_rect = wall
        
        

        
        
        