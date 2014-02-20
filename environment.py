import random
from character import *


class Environment(Character):
    def __init__(self, level, loc, *groups):
        super(Environment, self).__init__(level, loc)
        self.jump_hit = -10

    def update(self, dt, lvl, key, joy, screen, keys):
        self.kill_char()
        self.move()
        self.inertia()
        super(Environment, self).update(dt, lvl, key, joy, screen, keys)

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


class Fire(Environment):
    def __init__(self, lvl, loc, rect, *groups):
        super(Character, self).__init__(*groups)
        self.area = rect
        self.sheet = pygame.image.load('images/sprites/fire.png').convert_alpha()
        self.animTypes = 'idle_right'
        #self.animSurf, self.hitmask_dict = self.get_images(self.sheet, self.animTypes, )


class Wind(Environment):
    def __init__(self, lvl, loc, prop, rect, *groups):
        super(Character, self).__init__(*groups)
        self.prop = prop
        self.area = rect
        self.sheet = pygame.image.load('images/environment/wind.png').convert_alpha()
        self.animTypes = {'wind': [256, 33, 0.1, False, 0]}
        self.placeholder = self.sheet.subsurface(0, 0, 256, 33)
        self.animSurf, self.hitmask_dict = self.get_images(self.sheet, self.animTypes)
        self.image = self.animSurf['wind'].getCurrentFrame()
        super(Environment, self).__init__(lvl, loc, self.prop, *groups)
        self.pos_sprite()

    def animate(self):
        self.image = self.animSurf['wind'].getCurrentFrame()
        if self.animSurf['wind'].isFinished():
            self.pos_sprite()
            self.conductor.play()

    def pos_sprite(self):
        random.seed()
        x = random.randint(self.area.x, self.area.x + self.area.width)
        y = random.randint(self.area.y, self.area.y + self.area.height)
        self.rect.topleft = (x, y)

    def push(self, lvl):
        if lvl.hero.rect.colliderect(self.area):
            lvl.hero.rect.x -= 2

    def update(self, dt, lvl, key, joy, screen, keys):
        self.animate()
        self.push(lvl)