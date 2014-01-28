from character import *

class para_layer_1(pygame.sprite.Sprite):
    def __init__(self, image, *groups):
        super(para_layer_1, self).__init__(*groups)
        self.image = image