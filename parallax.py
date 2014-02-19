from character import *


class ParaLayer(pygame.sprite.Sprite):
    def __init__(self, image, start, speed, i, offset, *groups):
        super(ParaLayer, self).__init__(*groups)
        self.start = start
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = start
        self.speed = speed
        self.floor_detect_rects = False
        self.name = i
        self.offset = offset

    def update(self, dt, lvl, key, joysticks, screen, keys):
        self.move(lvl)

    def move(self, lvl):
        if lvl.tilemap.viewport.x > 0 and lvl.tilemap.viewport.x < lvl.tilemap.px_width - lvl.tilemap.view_w:
            self.rect.x = (lvl.tilemap.viewport.x // self.speed) * -1
        if lvl.tilemap.viewport.y > 0 and lvl.tilemap.viewport.y < lvl.tilemap.px_height - lvl.tilemap.view_h:
            dist = ((lvl.tilemap.viewport.y - 880) // self.speed) * -1
            self.rect.y = self.start[1] + dist

    def para_blit(self, screen, level):
        repeat = level.tilemap.px_width // self.rect.width
        for i in range(repeat):
            screen.blit(self.image, (self.rect.x + (self.rect.width * i), self.rect.y))
        screen.blit(self.image, (self.rect.x - self.rect.width, self.rect.y))