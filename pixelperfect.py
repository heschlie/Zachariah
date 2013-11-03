import pygame, sys
from pygame.locals import *

def check_collision(obj1,obj2):
    """checks if two objects have collided, using hitmasks"""
    try:
        rect1, rect2, hm1, hm2 = obj1.rect, obj2.rect, obj1.hitmask, obj2.hitmask
    except AttributeError:
        return False
    rect=rect1.clip(rect2)
    if rect.width==0 or rect.height==0:
        return False
    x1,y1,x2,y2 = rect.x-rect1.x,rect.y-rect1.y,rect.x-rect2.x,rect.y-rect2.y
    for x in xrange(rect.width):
        for y in xrange(rect.height):
            if hm1[x1+x][y1+y] and hm2[x2+x][y2+y]:
                print x1, y1
                return True
            else:
                continue
    return False

def load_image(name, colorkey=None, alpha=False):
    """loads an image into memory"""
    try:
        image = pygame.image.load(name)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    if alpha:
        image = image.convert_alpha()
    else:
        image=image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    print "Success"
    return image, image.get_rect()