from character import *


class Monster(Character):
    def __init__(self, lvl, loc, properties, *groups):
        self.image = self.animSurf['idle_left'].getCurrentFrame()
        super(Monster, self).__init__(lvl, loc, properties)
        self.dir = 'left'
        self.patrol_distance = 160
        self.jump_hit = 0
        
    def update(self, dt, lvl, key, joy, screen, keys):
        self.kill_char()
        if self.damage:
            self.damage_animation()
        if not self.damage:
            self.move()
        self.inertia()
        super(Monster, self).update(dt, lvl, key, joy, screen, keys)
        
    def move(self):
        right = 'right'
        left = 'left'
        if self.rect.left - self.start[0] < -self.patrol_distance:
            self.dir = right
        if self.rect.right - self.start[0] > self.patrol_distance:
            self.dir = left
        #setting directions for idle
        if self.dir == 'left':
            self.image = self.animSurf['idle_left'].getCurrentFrame()
            self.hitmask = self.hitmask_dict['idle_left'][self.animSurf['idle_left']._propGetCurrentFrameNum()]
        if self.dir == 'right':
            self.image = self.animSurf['idle_right'].getCurrentFrame()
            self.hitmask = self.hitmask_dict['idle_right'][self.animSurf['idle_right']._propGetCurrentFrameNum()]
        if self.dir == left and self.max_speed > 0:
            self.image = self.animSurf['idle_left'].getCurrentFrame()
            self.hitmask = self.hitmask_dict['idle_left'][self.animSurf['idle_left']._propGetCurrentFrameNum()]
            self.x_vel -= self.speed
        if self.dir == right and self.max_speed > 0:
            self.image = self.animSurf['idle_right'].getCurrentFrame()
            self.hitmask = self.hitmask_dict['idle_right'][self.animSurf['idle_right']._propGetCurrentFrameNum()]
            self.x_vel += self.speed

    def kill_char(self):
        if self.dead:
            self.hitmask = self.blank_hitmask
            self.kill()
        
        
class Walker(Monster):
    def __init__(self, lvl, loc, properties, *groups):
        super(Character, self).__init__(*groups)
        self.sheet = pygame.image.load('images/sprites/walker.png').convert_alpha()
        self.animTypes = self.anim_dict()
        self.placeholder = self.sheet.subsurface(0, 0, 32, 32)
        self.animSurf, self.hitmask_dict = self.get_images(self.sheet, self.animTypes)
        super(Walker, self).__init__(lvl, loc, properties)
        self.hp = 2
        self.jump_hit = 18
        
    def anim_dict(self):
        animTypes = {
            'idle_right': [32, 32, 0.175, True, 0],
            'blank1_right': [32, 32, 0.175, True, 32],
            'blank2_right': [32, 32, 0.175, True, 64],
            'blank3_right': [32, 32, 0.175, True, 96],
            'damage_right': [32, 32, 0.175, False, 128],
            'dead_right': [32, 32, 0.175, False, 160]
        }
        return animTypes


class Standing(Monster):
    def __init__(self, lvl, loc, properties, *groups):
        super(Character, self).__init__(*groups)
        self.sheet = pygame.image.load('images/sprites/stander.png').convert_alpha()
        self.animTypes = self.anim_dict()
        self.placeholder = self.sheet.subsurface(0, 0, 32, 32)
        self.animSurf, self.hitmask_dict = self.get_images(self.sheet, self.animTypes)
        super(Standing, self).__init__(lvl, loc, properties)
        self.max_speed = 0
        self.hp = 5
        self.jump_hit = 18
        
    def anim_dict(self):
        animTypes = {
            'idle_right': [32, 32, 0.175, True, 0],
            'blank1_right': [32, 32, 0.175, True, 32],
            'blank2_right': [32, 32, 0.175, True, 64],
            'blank3_right': [32, 32, 0.175, True, 96],
            'damage_right': [32, 32, 0.175, False, 128],
            'dead_right': [32, 32, 0.175, False, 160]
        }
        return animTypes


class Jumper(Monster):
    def __init__(self, lvl, loc, properties, *groups):
        super(Character, self).__init__(*groups)
        self.sheet = pygame.image.load('images/sprites/jumper.png').convert_alpha()
        self.animTypes = self.anim_dict()
        self.placeholder = self.sheet.subsurface(0, 0, 32, 32)
        self.animSurf, self.hitmask_dict = self.get_images(self.sheet, self.animTypes)
        super(Jumper, self).__init__(lvl, loc, properties)
        self.hp = 2
        self.jump_hit = 18
        
    def anim_dict(self):
        animTypes = {
            'idle_right': [32, 32, 0.175, True, 0],
            'blank1_right': [32, 32, 0.175, True, 32],
            'blank2_right': [32, 32, 0.175, True, 64],
            'blank3_right': [32, 32, 0.175, True, 96],
            'damage_right': [32, 32, 0.175, False, 128],
            'dead_right': [32, 32, 0.175, False, 160],
            'something_right': [32, 32, 0.175, False, 192]
        }
        return animTypes

    def update(self, dt, lvl, key, joy, screen, keys):
        super(Jumper, self).update(dt, lvl, key, joy, screen, keys)
        self.jump()