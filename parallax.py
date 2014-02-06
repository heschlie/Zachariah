from character import *


class ParaLayer(pygame.sprite.Sprite):
    def __init__(self, image, start, speed, i, *groups):
        super(ParaLayer, self).__init__(*groups)
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.bottomleft = start
        self.speed = speed
        self.floor_detect_rects = False
        self.name = i

    def update(self, dt, lvl, key, joysticks, screen, keys):
        self.move(lvl, screen)

    def move(self, lvl, screen):
        if lvl.tilemap.viewport.x > 0 and lvl.tilemap.viewport.x < lvl.tilemap.px_width - lvl.tilemap.view_w:
            self.rect.x -= (lvl.hero.x_vel // self.speed)
        # if lvl.tilemap.viewport.y > 0 and lvl.tilemap.viewport.y < lvl.tilemap.px_height - lvl.tilemap.view_h:
        #     if lvl.hero.y_vel <= 1:
        #         self.rect.y += 3 // self.speed
        #     if lvl.hero.y_vel >= 1:
        #         self.rect.y -= 3 // self.speed