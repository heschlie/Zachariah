import pygame, sys, player
from pygame.locals import *
from pixelperfect import *
import tiledtmxloader
#from main import *

def load(world):
    pygame.init()
    screen = pygame.display.get_surface()
    
    print world
    clock = pygame.time.Clock()
    hero = player.Player()
    lvl = Level(hero)
    
    lvl.set_player_loc(hero, 100, 100)
    
    while True:
        dt = 60
        clock.tick(dt)
        
        hero.update(dt/1000., lvl)
        update_viewport(hero, lvl)
        
        lvl.sprite_layers[0].add_sprite(hero._sprite)
        
        screen.fill((0,100,0))
        
        for layer in lvl.sprite_layers:
            if layer.is_object_group:
                continue
            else:
                lvl.renderer.render_layer(screen, layer)
        
        #screen.blit(lvl.lvl_bg, lvl.rect)
        #screen.blit(hero.image, hero.rect)
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
                
def update_viewport(hero, lvl):
    if hero._sprite.rect.centerx <= 640 and hero._sprite.rect.centery <= 370:
        #Top left
        lvl.renderer.set_camera_position(640, 370)
    elif hero._sprite.rect.centerx >= lvl.lvl_map.pixel_width - 640 and hero._sprite.rect.centery >= lvl.lvl_map.pixel_height - 370:
        #Bottom right
        lvl.renderer.set_camera_position(lvl.lvl_map.pixel_width - 640, lvl.lvl_map.pixel_height - 370)
    elif hero._sprite.rect.centerx <= 640 and hero._sprite.rect.centery >= lvl.lvl_map.pixel_height - 370:
        #Bottom left
        lvl.renderer.set_camera_position(640, lvl.lvl_map.pixel_height - 370)
    elif hero._sprite.rect.centerx >= lvl.lvl_map.pixel_width - 640 and hero._sprite.rect.centery <= 370:
        #Top Right
        lvl.renderer.set_camera_position(lvl.lvl_map.pixel_width - 640, 370)
    elif hero._sprite.rect.centerx <= 640:
        #Left
        lvl.renderer.set_camera_position(640, hero._sprite.rect.centery)
    elif hero._sprite.rect.centerx >= lvl.lvl_map.pixel_width - 640:
        #Right
        lvl.renderer.set_camera_position(lvl.lvl_map.pixel_width - 640, hero._sprite.rect.centery)
    elif hero._sprite.rect.centery <= 370:
        #Top
        lvl.renderer.set_camera_position(hero._sprite.rect.centerx, 370)
    elif hero._sprite.rect.centery >= lvl.lvl_map.pixel_height - 370:
        #bottom
        lvl.renderer.set_camera_position(hero._sprite.rect.centerx, lvl.lvl_map.pixel_height -370)
    else:
        lvl.renderer.set_camera_position(hero._sprite.rect.centerx, hero._sprite.rect.centery)

class Level(object):
    
    def __init__(self, hero):

        #self.lvl_bg, self.rect = load_image('test_level.png', None, True)
        #self.hitmask = pygame.surfarray.array_alpha(self.lvl_bg)
        
        self.lvl_map = tiledtmxloader.tmxreader.TileMapParser().parse_decode("levels/test/untitled.tmx")
        
        self.resources = tiledtmxloader.helperspygame.ResourceLoaderPygame()
        self.resources.load(self.lvl_map)
        
        self.renderer = tiledtmxloader.helperspygame.RendererPygame()
        
        cam_x = hero.rect.centerx
        cam_y = hero.rect.centery
        
        self.renderer.set_camera_position_and_size(cam_x, cam_y, 1280, 720)
        
        self.sprite_layers = tiledtmxloader.helperspygame.get_layers_from_map(self.resources)
        self.sprite_layers = [layer for layer in self.sprite_layers if not layer.is_object_group]
        
    def set_player_loc(self, player, x, y):
        player.rect.center = (x, y)