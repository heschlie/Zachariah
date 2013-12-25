from character import *


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
        self.dead = False
        
    def update(self, dt, lvl, key, joy):
        self.get_events(key, joy)
        self.check_keys()
        self.inertia()
        super(Player, self).update(dt, lvl, key, joy)
        lvl.tilemap.set_focus(self.rect.centerx, self.rect.centery)
        self.max_speed = 3
        self.jmp_damage(lvl)
        
    def check_keys(self):
        #setting directions for idle
        if self.dir == 'left':
            self.image = self.animSurf['idle_left'].getCurrentFrame()
            self.hitmask = self.hitmask_dict['idle_left'][self.animSurf['idle_left']._propGetCurrentFrameNum()]
        if self.dir == 'right':
            self.image = self.animSurf['idle_right'].getCurrentFrame()
            self.hitmask = self.hitmask_dict['idle_right'][self.animSurf['idle_right']._propGetCurrentFrameNum()]
        if self.run:
            self.max_speed = 6
        if self.direction == 'left':
            if abs(self.x_vel) > 1:
                self.image = self.animSurf['walk_left'].getCurrentFrame()
                self.hitmask = self.hitmask_dict['walk_left'][self.animSurf['walk_left']._propGetCurrentFrameNum()]
            if abs(self.x_vel) > 4:
                self.image = self.animSurf['run_left'].getCurrentFrame()
                self.hitmask = self.hitmask_dict['run_left'][self.animSurf['run_left']._propGetCurrentFrameNum()]
            self.dir = 'left'
            self.x_vel -= self.speed
        if self.direction == 'right':
            if self.x_vel > 1:
                self.image = self.animSurf['walk_right'].getCurrentFrame()
                self.hitmask = self.hitmask_dict['walk_right'][self.animSurf['walk_right']._propGetCurrentFrameNum()]
            if self.x_vel > 4:
                self.image = self.animSurf['run_right'].getCurrentFrame()
                self.hitmask = self.hitmask_dict['run_right'][self.animSurf['run_right']._propGetCurrentFrameNum()]
            self.dir = 'right'
            self.x_vel += self.speed

    def inertia(self):
        max_speed = self.max_speed  # + abs(self.plat_speed)
        if abs(self.x_vel) - self.x_det > max_speed:
            if self.x_vel > 0:
                self.x_vel -= (self.x_det * 2)
            if self.x_vel < 0:
                self.x_vel += (self.x_det * 2)
        if self.x_vel > 0 and self.direction == '' or self.x_vel > max_speed:
            self.x_vel -= self.x_det
        if self.x_vel < 0 and self.direction == '' or self.x_vel < (max_speed * -1):
            self.x_vel += self.x_det
        #self.x_vel += self.plat_speed

    def get_events(self, key, joy):
        self.run = self.get_run(key, joy)
        self.direction = self.get_direction(key, joy)

    def get_direction(self, key, joy):
        direction = ''
        for event in joy:
            if event.get_hat(0) == (-1, 0):
                direction = 'left'
            elif event.get_hat(0) == (1, 0):
                direction = 'right'
        if key[pygame.K_LEFT]:
            direction = 'left'
        elif key[pygame.K_RIGHT]:
            direction = 'right'
        return direction

    def get_run(self, key, joy):
        run = False
        for event in joy:
            if event.get_button(2):
                run = True
        if key[pygame.K_LSHIFT]:
            run = True
        return run

    def jmp_damage(self, level):
        x_vel = int(self.x_vel)
        y_vel = int(self.y_vel)
        mob_offset = 0
        test = pygame.Rect((self.rect.x + x_vel, self.rect.y + y_vel), (self.rect.width, self.rect.height))
        for mob in level.enemies:
            mask_test = test.x - mob.rect.x, test.y - mob.rect.y
            if self.rect.bottom < mob.rect.top + mob.jump_hit and \
                    mob.hitmask.overlap(self.hitmask, mask_test) and self.fall:
                mob_offset = mob.rect.centerx - self.rect.centerx
                mob.take_damage(1, mob_offset, 8)
                self.bounce()
                print mob.hp
            elif mob.hitmask.overlap(self.hitmask, mask_test):
                self.hp -= 1

    def bounce(self):
        self.y_vel = -4

    def check_alive(self):
        if self.hp <= 0:
            self.dead = True