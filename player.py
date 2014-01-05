from character import *


class Player(Character):
    def __init__(self, lvl, loc, *groups):
        super(Character, self).__init__(*groups)
        self.sheet = pygame.image.load('images/sprites/char.png').convert_alpha()
        animTypes = 'idle_right walk_right run_right jump_right fall_right tred_right swim_right ladder_right ' \
                    'stop_right damage_right'.split()
        self.placeholder = self.sheet.subsurface(0, 0, 32, 64)
        self.animSurf, self.hitmask_dict = self.get_images(self.sheet, animTypes, 42, 64)
        self.image = self.animSurf['idle_right'].getCurrentFrame()
        super(Player, self).__init__(lvl, loc)
        self.rect.center = loc
        self.ears = Ears(lvl, (self.rect.x, self.rect.y), lvl.sprites)
        self.direction = 'right'
        self.fat_mask = self.gen_fat_mask()
        self.jump_power = -8.75
        self.hp = 3
        self.max_speed = 3
        
    def update(self, dt, lvl, key, joy, screen, keys):
        if self.damage:
            self.damage_animation()
        if not self.damage:
            self.get_events(key, keys, joy)
            self.move()
            self.inertia()
        super(Player, self).update(dt, lvl, key, joy, screen, keys)
        self.ears.set_pos(self.rect.topleft)
        lvl.tilemap.set_focus(self.rect.centerx, self.rect.centery)
        self.max_speed = 3
        self.jmp_damage(lvl)

    def gen_fat_mask(self):
        mask = pygame.mask.Mask((self.rect.width, self.rect.height))
        mask.clear()
        for y in range(self.rect.height):
            for x in range(self.rect.width):
                if x > 4 < 38 and y < 59:
                    mask.set_at((x, y), 1)
        return mask
        
    def move(self):
        #setting directions for idle
        if self.dir == 'left':
            self.image = self.animSurf['idle_left'].getCurrentFrame()
            frame = self.animSurf['idle_left']._propGetCurrentFrameNum()
            self.hitmask = self.hitmask_dict['idle_left'][frame]
        if self.dir == 'right':
            self.image = self.animSurf['idle_right'].getCurrentFrame()
            frame = self.animSurf['idle_right']._propGetCurrentFrameNum()
            self.hitmask = self.hitmask_dict['idle_right'][frame]
        if self.run:
            self.max_speed = 6
        if self.direction == 'left':
            if abs(self.x_vel) > 1:
                self.image = self.animSurf['walk_left'].getCurrentFrame().copy()
                frame = self.animSurf['walk_left']._propGetCurrentFrameNum()
                self.hitmask = self.hitmask_dict['walk_left'][frame]
            if abs(self.x_vel) > 4:
                self.image = self.animSurf['run_left'].getCurrentFrame().copy()
                frame = self.animSurf['run_left']._propGetCurrentFrameNum()
                self.hitmask = self.hitmask_dict['run_left'][frame]
            self.dir = 'left'
            self.x_vel -= self.speed
        if self.direction == 'right':
            if self.x_vel > 1:
                self.image = self.animSurf['walk_right'].getCurrentFrame().copy()
                frame = self.animSurf['walk_right']._propGetCurrentFrameNum()
                self.hitmask = self.hitmask_dict['walk_right'][frame]
            if self.x_vel > 4:
                self.image = self.animSurf['run_right'].getCurrentFrame().copy()
                frame = self.animSurf['run_right']._propGetCurrentFrameNum()
                self.hitmask = self.hitmask_dict['run_right'][frame]
            self.dir = 'right'
            self.x_vel += self.speed

    def inertia(self):
        max_speed = self.max_speed
        if abs(self.x_vel) - self.x_det > max_speed:
            if self.x_vel > 0:
                self.x_vel -= (self.x_det * 2)
            if self.x_vel < 0:
                self.x_vel += (self.x_det * 2)
        if self.x_vel > 0 and self.direction == '' or self.x_vel > max_speed:
            self.x_vel -= self.x_det
        if self.x_vel < 0 and self.direction == '' or self.x_vel < (max_speed * -1):
            self.x_vel += self.x_det

    def get_events(self, key, keys, joy):
        self.jump_keys(keys)
        self.run = self.get_run(key, joy)
        self.direction = self.get_direction(key, joy)
    
    def jump_keys(self, keys):
        for event in keys:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.jump()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.jump_cut()
            elif event.type == JOYBUTTONDOWN:
                if event.button == 0:
                    self.jump()
            elif event.type == JOYBUTTONUP:
                if event.button == 0:
                    self.jump_cut()

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
        for mob in level.enemies:
            if self.sprite_collide(self, mob, (x_vel, y_vel)):
                if self.rect.bottom < mob.rect.top + mob.jump_hit and self.fall and self.y_vel > 0:
                    mob_offset = mob.rect.centerx - self.rect.centerx
                    mob.take_damage(1, mob_offset, 8)
                    self.bounce()
                else:
                    offset = self.rect.centerx - mob.rect.centerx
                    self.take_damage(1, offset, 1, 4)

    def take_damage(self, damage, offset, pushx, pushy):
        if offset >= 3:
            self.dir = 'left'
            self.x_vel = pushx
        elif offset <= -3:
            self.dir = 'right'
            self.x_vel = -pushx
        #self.hp -= damage
        self.fall = True
        self.y_vel = -pushy
        self.damage = True
        self.animSurf['damage_right'].play()
        self.animSurf['damage_left'].play()
        self.ears.animSurf['damage_right'].play()
        self.ears.animSurf['damage_left'].play()

    def damage_animation(self):
        self.hitmask = self.blank_hitmask
        if self.dir == 'left':
            self.image = self.animSurf['damage_left'].getCurrentFrame()
            self.ears.image = self.ears.animSurf['damage_left'].getCurrentFrame()
            if self.animSurf['damage_left'].isFinished():
                self.damage = False
        elif self.dir == 'right':
            self.image = self.animSurf['damage_right'].getCurrentFrame()
            self.ears.image = self.ears.animSurf['damage_right'].getCurrentFrame()
            if self.animSurf['damage_right'].isFinished():
                self.damage = False

    def bounce(self):
        self.y_vel = -5


class Ears(Character):
    def __init__(self, lvl, loc, *groups):
        super(Character, self).__init__(*groups)
        self.sheet = pygame.image.load('images/sprites/char_ears.png').convert_alpha()
        self.placeholder = self.sheet.subsurface(0, 0, 42, 64)
        animTypes = 'idle_right walk_right run_right jump_right fall_right tred_right swim_right ladder_right ' \
                    'stop_right damage_right'.split()
        self.animSurf, self.hitmask_dict = self.get_images(self.sheet, animTypes, 42, 64)
        self.image = self.animSurf['idle_right'].getCurrentFrame()
        super(Ears, self).__init__(lvl, loc)
        self.rect.topleft = loc
        self.hitmask.clear()

    def update(self, dt, lvl, key, joy, screen, keys):
        if not lvl.hero.damage:
            self.animate(lvl)

    def animate(self, lvl):
        if lvl.hero.dir == 'left':
            frame = lvl.hero.animSurf['idle_left']._propGetCurrentFrameNum()
            self.image = self.animSurf['idle_left'].getFrame(frame)

        if lvl.hero.dir == 'right':
            frame = lvl.hero.animSurf['idle_right']._propGetCurrentFrameNum()
            self.image = self.animSurf['idle_right'].getFrame(frame)

        if lvl.hero.direction == 'left':
            if abs(lvl.hero.x_vel) > 1:
                frame = lvl.hero.animSurf['walk_left']._propGetCurrentFrameNum()
                self.image = self.animSurf['walk_left'].getFrame(frame)

            if abs(lvl.hero.x_vel) > 4:
                frame = lvl.hero.animSurf['run_left']._propGetCurrentFrameNum()
                self.image = self.animSurf['run_left'].getFrame(frame)

        if lvl.hero.direction == 'right':
            if lvl.hero.x_vel > 1:
                frame = lvl.hero.animSurf['walk_right']._propGetCurrentFrameNum()
                self.image = self.animSurf['walk_right'].getFrame(frame)

            if lvl.hero.x_vel > 4:
                frame = lvl.hero.animSurf['run_right']._propGetCurrentFrameNum()
                self.image = self.animSurf['run_right'].getFrame(frame)

    def set_pos(self, loc):
        self.rect.topleft = loc