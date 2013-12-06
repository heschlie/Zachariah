import pygame, sys
from pygame.locals import *
from pixelperfect import *
import tmx
import pyganim


class Character(pygame.sprite.Sprite):
    def __init__(self, lvl, loc, *groups):
        self.conductor = pyganim.PygConductor(self.animSurf)
        self.image = self.face_right
        self.rect = self.image.get_rect()
        self.hitmask = pygame.mask.from_surface(self.image, 127)
        self.dir = 'right'
        self.fall = False
        self.platform = False
        self.speed = 3
        self.jump_power = -8.75
        self.jump_cut_magnitude = -3
        self.grav = 0.22
        self.y_vel = self.x_vel = 0
        self.setup_collision_rects()
        
    def update(self, dt, lvl, key):
        self.detect_wall(lvl)
        self.detect_ground(lvl)
        self.physics_update()
        
    def setup_collision_rects(self):
        self.reset_wall_floor_rects()
        self.fat_mask = pygame.Mask(self.rect.size)
        self.fat_mask.fill()
        self.wall_detect_mask = pygame.Mask(self.wall_detect_rect.size)
        self.wall_detect_mask.fill()
        self.floor_detect_mask = pygame.Mask((self.rect.width-10, 1))
        self.floor_detect_mask.fill()
        self.collide_ls = []
        
    def detect_ground(self, level):
        if not self.fall:
            self.grounded(level)
        else:
            self.airborne(level)
        self.reset_wall_floor_rects()
              
    def grounded(self, level):
        change = None
        pads_on = [False, False]
        for i, floor in enumerate(self.floor_detect_rects):
            collide, pads_on = self.check_floor_initial(pads_on, (i, floor), level)
            if collide:
                change = self.check_floor_final(collide, (i, floor), change, level)
        for i, floor in enumerate(self.floor_detect_rects):
            collide, pads_on = self.check_floor_initial_platform(pads_on, (i, floor), level)
            if collide:
                change = self.check_floor_final_platform(collide, (i, floor), change, level)
        if pads_on[0]^pads_on[1]:
            change = self.detect_glitch_fix(pads_on,change,level)
        if change != None:
            self.rect.y = int(change - self.rect.height)
        else:
            self.fall = True
                
    def check_floor_initial(self, pads_on, pad_details, level):
        i, floor = pad_details
        collide = []
        for cell in level.rect_dict:
            if floor.colliderect(level.rect_dict[cell]):
                collide.append(cell)
                pads_on[i] = True     
        return collide, pads_on
    
    def check_floor_initial_platform(self, pads_on, pad_details, level):
        i, floor = pad_details
        collide = []
        for plat in level.platforms:
            if floor.colliderect(plat.rect):
                collide.append(plat)
                pads_on[i] = True
            return collide, pads_on
         
    def check_floor_final(self, collide, pad_details, change, level):
        i, floor = pad_details
        for key in collide:
            cell_heights = level.height_dict[key]
            x_in_cell = floor.x - key[0] * level.tilemap.layers['terrain'].tile_width
            offset = cell_heights[x_in_cell]
            if change == None:
                change = (key[1] + 1) * level.tilemap.layers['terrain'].tile_height - offset
            else:
                change = min((key[1] + 1) * level.tilemap.layers['terrain'].tile_height - offset, change)
        return change
    
    def check_floor_final_platform(self, collide, pad_details, change, level):
        i, floor = pad_details
        for plat in collide:
            x_in_plat = floor.x - plat.rect.x
            offset = plat.height_map[x_in_plat]
            if change == None:
                change = (plat.rect.bottom) - offset
            else:
                change = min((plat.rect.bottom) - offset, change)
        return change
    
    def detect_wall(self, level):
        if not self.fall:
            rect,mask = self.wall_detect_rect,self.wall_detect_mask
        else:
            rect,mask = self.rect,self.fat_mask
        if self.collide_with(level,rect,mask,(int(self.x_vel),0)):
            #self.x_vel = self.adjust_pos(level,rect,mask,[int(self.x_vel),0],0)
            self.x_vel = 0
        elif self.collide_with_platform(level, rect, mask, (int(self.x_vel), 0)):
            self.x_vel = 0            
        self.rect.x += int(self.x_vel)
        self.reset_wall_floor_rects()
      
    def reset_wall_floor_rects(self):
        flr = (pygame.Rect((self.rect.x+7,self.rect.y),(1,self.rect.height+16)),
               pygame.Rect((self.rect.right-8,self.rect.y),(1,self.rect.height+16)))
        wall = pygame.Rect(self.rect.x+6,self.rect.bottom-15,self.rect.width-6,1)
        self.floor_detect_rects = flr
        self.wall_detect_rect = wall
        
    def airborne(self, level):
        new = self.rect
        mask = self.floor_detect_mask
        check = (pygame.Rect(self.rect.x+1,self.rect.y,self.rect.width-1,1),
                 pygame.Rect(self.rect.x+1,self.rect.bottom-1,self.rect.width-2,1))
        stop_fall = False
        for rect in check:
            if self.collide_with(level, rect, mask, [0, int(self.y_vel)]):
                #offset = [0, int(self.y_vel)]
                #self.y_vel = self.adjust_pos(level, rect, mask, offset, 1)
                self.y_vel = 0
                stop_fall = True
            if self.collide_with_platform(level, rect, mask, [0, int(self.y_vel)]):
                self.y_vel = 0
                stop_fall = True
                self.platform = True
            else:
                self.fall = True
                self.platform = False
        self.rect.y += int(self.y_vel)
        if stop_fall:
            self.fall = False
            
    def collide_with(self, level, rect, mask, offset):
        test = pygame.Rect((rect.x + offset[0], rect.y + offset[1]), rect.size)
        self.collide_ls = []
        for cell, rec in level.rect_dict.items():
            if test.colliderect(rec):
                level_rect = level.rect_dict[cell]
                mask_test = test.x - level_rect.x, test.y - level_rect.y
                level_mask = level.mask_dict[cell]
                if level_mask.overlap_area(mask, mask_test):
                    self.collide_ls.append(cell)
        return self.collide_ls
    
    def collide_with_platform(self, level, rect, mask, offset):
        test = pygame.Rect((rect.x + offset[0], rect.y + offset[1]), rect.size)
        for plat in level.platforms:
            if test.colliderect(plat.rect):
                mask_test = test.x - plat.rect.x, test.y - plat.rect.y
                if plat.hitmask.overlap(mask, mask_test):
                    return True
    
    # """Was unable to get this working properly, so I am simply setting the velocity
    # of the character to 0 when it detects a floor or wall.  I will change this if
    # problems arise."""
#     def adjust_pos(self, level, rect, mask, offset, off_ind):
#         offset[off_ind] += (1 if offset[off_ind] < 0 else -1)
#         while 1:
#             if any(self.collide_with(level, rect, mask, offset)):
#                 offset[off_ind] += (1 if offset[off_ind] < 0 else -1)
#                 if not offset[off_ind]:
#                     return 0
#                 else:
#                     return offset[off_ind]
    
    def physics_update(self):
        if self.fall:
            if self.y_vel < abs(10):
                self.y_vel += self.grav
        else:
            self.y_vel = 0
                
    def detect_glitch_fix(self,pads,change,level):
        """Fixes a glitch with the blit location that occurs on up-slopes when
        one detection bar hits a solid cell and the other doesn't. This could
        probably still be improved."""
        inc,index = ((1,0) if not pads[0] else (-1,1))
        detector = self.floor_detect_rects[index].copy()
        pad_details = (index,detector)
        old_change = change
        while detector.x != self.floor_detect_rects[not index].x:
            detector.x += inc
            collide = self.check_floor_initial([0,0],pad_details,level)[0]
            change = self.check_floor_final(collide,pad_details,change,level)
            if change < old_change:
                return change
        return old_change
    
    def detect_glitch_fix_platform(self, pads, change, level):
        inc, index = ((1,0) if not pads[0] else (-1,1))
        detector = self.floor_detect_rects[index].copy()
        pad_details = (index, detector)
        old_change = change
        while detector.x != self.floor_detect_rects[not index].x:
            detector.x += inc
            collide = self.check_floor_initial_platform([0,0], pad_details, level)
            change = self.check_floor_final_platform(collide, pad_details, change, level)
            if change < old_change:
                return change
        return old_change
        
    def jump(self):
        """Called when the player presses the jump key."""
        if not self.fall:
            self.y_vel = self.jump_power
            self.fall = True

    def jump_cut(self):
        """Called when the palyer releases the jump key before maximum height is
        reached."""
        if self.fall:
            if self.y_vel < self.jump_cut_magnitude:
                self.y_vel = self.jump_cut_magnitude

    def flip_anim(self, src):
        fliped = src.getCopy()
        fliped.flip(True, False)
        fliped.makeTransformsPermanent()
        return fliped
            

class Player(Character):
    def __init__(self, lvl, loc, *groups):
        super(Character, self).__init__(*groups)
        self.sheet = pygame.image.load('images/char.png').convert_alpha()
        self.placeholder = self.sheet.subsurface(0, 0, 32, 64)
        self.animSurf = self.get_images(self.sheet, 32, 64)
        super(Player, self).__init__(lvl, loc)
        self.rect.center = loc
        
    def update(self, dt, lvl, key):
        self.check_keys(key)
        super(Player, self).update(dt, lvl, key)
        lvl.tilemap.set_focus(self.rect.centerx, self.rect.centery)
        self.speed = 3
        
    def check_keys(self, key):
        self.conductor.play()
        self.x_vel = 0
        #setting directions for idle
        if self.dir == 'left':
            self.image = self.face_left
        if self.dir == 'right':
            self.image = self.face_right
        if key[pygame.K_LSHIFT]:
            self.speed = 6
        if key[pygame.K_LEFT]:
            if self.speed == 3:
                self.image = self.animSurf['walk_left'].getCurrentFrame()
                #print self.animSurf['walk_left']._propGetCurrentFrameNum()
            if self.speed == 6:
                self.image = self.animSurf['run_left'].getCurrentFrame()
            self.dir = 'left'
            self.x_vel -= self.speed
        if key[pygame.K_RIGHT]:
            if self.speed == 3:
                self.image = self.animSurf['walk_right'].getCurrentFrame()
            if self.speed == 6:
                self.image = self.animSurf['run_right'].getCurrentFrame()
            self.dir = 'right'
            self.x_vel += self.speed
        self.hitmask = pygame.mask.from_surface(self.image, 127)

    def get_images(self, sheet, imgWidth, imgHeight):
        self.face_right = self.sheet.subsurface((0, 0, 32, 64))
        self.face_left = pygame.transform.flip(self.face_right, True, False)
        sheetRect = sheet.get_rect()
        animSurf = {}
        animTypes = 'idle_right walk_right run_right jump_right fall_right tred_right swim_right stop_right ' \
                    'damage_right'.split()
        animFlips = 'idle_left walk_left run_left jump_left fall_left tred_left swim_left stop_left damage_left'.split()
        placeholder = [(self.placeholder, 0.175), (self.placeholder, 0.175)]
        for y, animType in enumerate(animTypes):
            imageAndDuration = []
            for x in range(sheetRect.width/imgWidth):
                image = self.sheet.subsurface(imgWidth*x, imgHeight*y, imgWidth, imgHeight)
                for i in range(imgHeight):
                    z = False
                    for j in range(imgWidth):
                        if image.get_at((j, i))[3] > 0:
                            imageAndDuration.append((image, 0.175))
                            z = True
                            break
                    if z:
                        break
            if imageAndDuration:
                animSurf[animType] = pyganim.PygAnimation(imageAndDuration)
            else:
                animSurf[animType] = pyganim.PygAnimation(placeholder)
        #flipping the right animations to create the left ones
        for i, src in enumerate(animTypes):
            animSurf[animFlips[i]] = self.flip_anim(animSurf[src])
        return animSurf