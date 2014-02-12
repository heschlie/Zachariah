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
            self.rect.x = (lvl.tilemap.viewport.x // self.speed) * -1
        # if lvl.tilemap.viewport.y > 0 and lvl.tilemap.viewport.y < lvl.tilemap.px_height - lvl.tilemap.view_h:
        #     dist = ((lvl.tilemap.viewport.y) // self.speed)
        #     self.rect.y = dist