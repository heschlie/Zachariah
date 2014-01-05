from character import *


class NPC(Character):
    def __init__(self, lvl, loc, *groups):
        self.image = self.animSurf['idle_left'].getCurrentFrame()
        super(NPC, self).__init__(lvl, loc)
        self.dir = 'left'
        self.start = loc
        self.rect.center = self.start
        self.patrol_distance = 0

    def update(self, dt, lvl, key, joy, screen, keys):
        self.move()
        super(NPC, self).update(dt, lvl, key, joy, screen, keys)

    def move(self):
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
        if self.dir == left and self.max_speed > 0:
            self.image = self.animSurf['idle_left'].getCurrentFrame()
            self.hitmask = self.hitmask_dict['idle_left'][self.animSurf['idle_left']._propGetCurrentFrameNum()]
            self.x_vel -= self.speed
        if self.dir == right and self.max_speed > 0:
            self.image = self.animSurf['idle_right'].getCurrentFrame()
            self.hitmask = self.hitmask_dict['idle_right'][self.animSurf['idle_right']._propGetCurrentFrameNum()]
            self.x_vel += self.speed


class DinoMale(NPC):
    def __init__(self, lvl, loc, *groups):
        super(Character, self).__init__(*groups)
        self.sheet = pygame.image.load('images/sprites/dino_male.png').convert_alpha()
        self.animTypes = 'idle_right walk_right'.split()
        self.placeholder = self.sheet.subsurface(0, 0, 64, 64)
        self.animSurf, self.hitmask_dict = self.get_images(self.sheet, self.animTypes, 72, 64)
        super(DinoMale, self).__init__(lvl, loc)
        self.max_speed = 0