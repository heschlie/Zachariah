from character import *


class ParaLayer(pygame.sprite.Sprite):
    def __init__(self, image, start, speed, *groups):
        super(ParaLayer, self).__init__(*groups)
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = start
        self.speed = speed
        self.floor_detect_rects = False

    def update(self, dt, lvl, key, joysticks, screen, keys):
        self.move(lvl, screen)

    def move(self, lvl, screen):
        screen_w = screen.get_width()
        if lvl.hero.rect.right > screen_w and lvl.hero.rect.left < lvl.tilemap.px_width - screen_w:
            self.rect.x -= (lvl.hero.x_vel // self.speed)