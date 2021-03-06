from character import *
from threading import Timer


class Player(Character):
    def __init__(self, lvl, loc, properties, *groups):
        super(Character, self).__init__(*groups)
        ears_prop = {}
        self.sheet = pygame.image.load('images/sprites/char.png').convert_alpha()
        animTypes = self.anim_dict()
        self.placeholder = self.sheet.subsurface(0, 0, 32, 64)
        self.animSurf, self.hitmask_dict = self.get_images(self.sheet, animTypes)
        self.image = self.animSurf['idle_right'].getCurrentFrame()
        super(Player, self).__init__(lvl, loc, properties)
        self.ears = Ears(lvl, (self.rect.x, self.rect.y), ears_prop, lvl.sprites)
        self.direction_x = 'right'
        self.direction_y = ''
        self.fat_mask = self.gen_fat_mask()
        self.jump_power = -8.75
        self.hp = 3
        self.max_speed = 3
        self.run = False
        # for i in self.animSurf.keys():
        #     print(i)

    def anim_dict(self):
        # Dict for get_images method, the key is the name of the animation, the list is [width, height,
        # speed, loop, Y in sheet]
        animTypes = {
            'idle_right': [42, 43, 0.175, True, 0],
            'walk_right': [42, 43, 0.175, True, 43],
            'run_right': [42, 43, 0.175, True, 86],
            'jump_right': [42, 43, 0.07, False, 129],
            'fall_right': [42, 43, 0.175, False, 172],
            'tred_right': [42, 43, 0.175, True, 215],
            'swim_right': [42, 43, 0.175, True, 258],
            'ladder_right': [42, 43, 0.175, True, 301],
            'stop_right': [42, 43, 0.175, True, 344],
            'damage_right': [42, 43, 0.175, False, 387],
            'attack_right': [104, 64, 0.175, False, 494]
        }
        return animTypes
        
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
        self.talk(lvl, key, joy, screen)
        if (self.animSurf['attack_left'].isFinished() or self.animSurf['attack_right'].isFinished()) and self.attacking:
            self.attacking = False

    def gen_fat_mask(self):
        mask = pygame.mask.Mask((self.rect.width, self.rect.height))
        mask.clear()
        for y in range(self.rect.height):
            for x in range(self.rect.width):
                if x > 4 and x < 37 and y < 55:
                    mask.set_at((x, y), 1)
        return mask

    def drop_set(self):
        self.drop = True
        stop = Timer(1.0, self.drop_stop)
        stop.start()

    def drop_stop(self):
        self.drop = False
        
    def move(self):
        # idle animation
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
        # Walking and running animations
        if self.direction_x == 'left':
            if abs(self.x_vel) > 1:
                self.image = self.animSurf['walk_left'].getCurrentFrame()
                frame = self.animSurf['walk_left']._propGetCurrentFrameNum()
                self.hitmask = self.hitmask_dict['walk_left'][frame]
            if abs(self.x_vel) > 4:
                self.image = self.animSurf['run_left'].getCurrentFrame()
                frame = self.animSurf['run_left']._propGetCurrentFrameNum()
                self.hitmask = self.hitmask_dict['run_left'][frame]
            self.dir = 'left'
            self.x_vel -= self.speed
        if self.direction_x == 'right':
            if self.x_vel > 1:
                self.image = self.animSurf['walk_right'].getCurrentFrame()
                frame = self.animSurf['walk_right']._propGetCurrentFrameNum()
                self.hitmask = self.hitmask_dict['walk_right'][frame]
            if self.x_vel > 4:
                self.image = self.animSurf['run_right'].getCurrentFrame()
                frame = self.animSurf['run_right']._propGetCurrentFrameNum()
                self.hitmask = self.hitmask_dict['run_right'][frame]
            self.dir = 'right'
            self.x_vel += self.speed
        # Jumping animations
        if self.dir == 'left':
            if self.fall and self.y_vel < 0:
                self.image = self.animSurf['jump_left'].getCurrentFrame()
                frame = self.animSurf['jump_left']._propGetCurrentFrameNum()
                self.hitmask = self.hitmask_dict['jump_left'][frame]
            if self.fall and self.y_vel >= 0:
                self.image = self.animSurf['fall_left'].getCurrentFrame()
                frame = self.animSurf['fall_left']._propGetCurrentFrameNum()
                self.hitmask = self.hitmask_dict['fall_left'][frame]
        if self.dir == 'right':
            if self.fall and self.y_vel < 0:
                self.image = self.animSurf['jump_right'].getCurrentFrame()
                frame = self.animSurf['jump_right']._propGetCurrentFrameNum()
                self.hitmask = self.hitmask_dict['jump_right'][frame]
            if self.fall and self.y_vel >= 0:
                self.image = self.animSurf['fall_right'].getCurrentFrame()
                frame = self.animSurf['fall_right']._propGetCurrentFrameNum()
                self.hitmask = self.hitmask_dict['fall_right'][frame]
        # Attacking animations
        if self.attacking and self.dir == 'left':
            self.image = self.animSurf['attack_left'].getCurrentFrame()
            frame = self.animSurf['attack_left']._propGetCurrentFrameNum()
            self.hitmask = self.hitmask_dict['attack_left'][frame]
        if self.attacking and self.dir == 'right':
            self.image = self.animSurf['attack_right'].getCurrentFrame()
            frame = self.animSurf['attack_right']._propGetCurrentFrameNum()
            self.hitmask = self.hitmask_dict['attack_right'][frame]
        if self.direction_y == 'down':
            pass

    def inertia(self):
        max_speed = self.max_speed
        if abs(self.x_vel) - self.x_det > max_speed:
            if self.x_vel > 0:
                self.x_vel -= (self.x_det * 2)
            if self.x_vel < 0:
                self.x_vel += (self.x_det * 2)
        if self.x_vel > 0 and self.direction_x == '' or self.x_vel > max_speed:
            self.x_vel -= self.x_det
        if self.x_vel < 0 and self.direction_x == '' or self.x_vel < (max_speed * -1):
            self.x_vel += self.x_det

    def get_events(self, key, keys, joy):
        self.action_keys(keys, key)
        self.run = self.get_run(key, joy)
        self.direction_x, self.direction_y = self.get_direction(key, joy, keys)
    
    def action_keys(self, keys, key):
        for event in keys:
            # Jump key
            if self.direction_y is not 'down':
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
            # Attack key
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RCTRL:
                    self.attack()
            elif event.type == pygame.JOYAXISMOTION:
                if event.axis == 2:
                    self.attack()

    def get_direction(self, key, joy, keys):
        direction_x = ''
        direction_y = ''
        for joystick in joy:
            if joystick.get_hat(0) == (-1, 0):
                direction_x = 'left'
            elif joystick.get_hat(0) == (1, 0):
                direction_x = 'right'
            if joystick.get_hat(0) == (0, 1):
                direction_y = 'up'
            elif joystick.get_hat(0) == (0, -1):
                direction_y = 'down'
            for event in keys:
                if event.type == pygame.JOYBUTTONDOWN:
                    if event.button == 0 and joystick.get_hat(0) == (0, -1):
                        self.drop_set()
        if key[pygame.K_LEFT]:
            direction_x = 'left'
        elif key[pygame.K_RIGHT]:
            direction_x = 'right'
        if key[pygame.K_UP]:
            direction_y = 'up'
        elif key[pygame.K_DOWN]:
            direction_y = 'down'
        if key[pygame.K_DOWN] and key[pygame.K_SPACE]:
            self.drop_set()
        return direction_x, direction_y

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

    def talk(self, level, key, joy, screen):
        x_vel = int(self.x_vel)
        y_vel = int(self.y_vel)
        for char in level.npc:
            if self.sprite_collide(self, char, (x_vel, y_vel)):
                if self.get_direction(key, joy) == 'up':
                    char.talk(screen)


class Ears(Character):
    def __init__(self, lvl, loc, properties, *groups):
        super(Character, self).__init__(*groups)
        self.sheet = pygame.image.load('images/sprites/char_ears.png').convert_alpha()
        self.placeholder = self.sheet.subsurface(0, 0, 42, 64)
        animTypes = self.anim_dict()
        self.animSurf, self.hitmask_dict = self.get_images(self.sheet, animTypes)
        self.image = self.animSurf['idle_right'].getCurrentFrame()
        super(Ears, self).__init__(lvl, loc, properties)
        self.rect.topleft = loc
        self.hitmask.clear()

    def anim_dict(self):
        animTypes = {
            'idle_right': [42, 64, 0.175, True, 0],
            'walk_right': [42, 64, 0.175, True, 64],
            'run_right': [42, 64, 0.175, True, 128],
            'jump_right': [42, 64, 0.175, True, 192],
            'fall_right': [42, 64, 0.175, True, 256],
            'tred_right': [42, 64, 0.175, True, 320],
            'swim_right': [42, 64, 0.175, True, 384],
            'ladder_right': [42, 64, 0.175, True, 448],
            'stop_right': [42, 64, 0.175, True, 512],
            'damage_right': [42, 64, 0.175, False, 576]
        }
        return animTypes

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

        if lvl.hero.direction_x == 'left':
            if abs(lvl.hero.x_vel) > 1:
                frame = lvl.hero.animSurf['walk_left']._propGetCurrentFrameNum()
                self.image = self.animSurf['walk_left'].getFrame(frame)

            if abs(lvl.hero.x_vel) > 4:
                frame = lvl.hero.animSurf['run_left']._propGetCurrentFrameNum()
                self.image = self.animSurf['run_left'].getFrame(frame)

        if lvl.hero.direction_x == 'right':
            if lvl.hero.x_vel > 1:
                frame = lvl.hero.animSurf['walk_right']._propGetCurrentFrameNum()
                self.image = self.animSurf['walk_right'].getFrame(frame)

            if lvl.hero.x_vel > 4:
                frame = lvl.hero.animSurf['run_right']._propGetCurrentFrameNum()
                self.image = self.animSurf['run_right'].getFrame(frame)
        if lvl.hero.dir == 'left':
            if lvl.hero.fall and lvl.hero.y_vel < 0:
                frame = lvl.hero.animSurf['jump_left']._propGetCurrentFrameNum()
                self.image = self.animSurf['jump_left'].getFrame(frame)

            if lvl.hero.fall and lvl.hero.y_vel >= 0:
                frame = lvl.hero.animSurf['fall_left']._propGetCurrentFrameNum()
                self.image = self.animSurf['fall_left'].getFrame(frame)

        if lvl.hero.dir == 'right':
            if lvl.hero.fall and lvl.hero.y_vel < 0:
                frame = lvl.hero.animSurf['jump_right']._propGetCurrentFrameNum()
                self.image = self.animSurf['jump_right'].getFrame(frame)

            if lvl.hero.fall and lvl.hero.y_vel >= 0:
                frame = lvl.hero.animSurf['fall_right']._propGetCurrentFrameNum()
                self.image = self.animSurf['fall_right'].getFrame(frame)


    def set_pos(self, loc):
        x = loc[0]
        y = loc[1] - 21
        self.rect.topleft = (x, y)