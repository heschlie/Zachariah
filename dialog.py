import pygame
import time
from pygame.locals import *
import level

def start_dialog(text, screen):
    paragraph = text.split()
    screen_size = screen.get_size()
    my_font = pygame.font.Font('freesansbold.ttf', 24)
    white = (255, 255, 255)
    dialog_object = []
    dialog_rects = []
    for i in range(5):
        dialog_object.append(my_font.render('', True, white))
        dialog_rects.append(dialog_object[i].get_rect())
    dialog_lines = ['', '', '', '', '']
    dialog_box = pygame.Rect(((screen_size[0] * .5) - 150, screen_size[1] - 225),
                             (700, (dialog_rects[0].height * 5) + 20))
    for i, rect in enumerate(dialog_rects):
        rect.topleft = (dialog_box.x + 10, (dialog_box.y + 10) + (i * 25))

    pygame.draw.rect(screen, (0, 0, 0), dialog_box)

    while True:
        for word in paragraph:
            if my_font.size(dialog_lines[0] + " " + word)[0] < dialog_box.width - 20:
                dialog_lines[0] = dialog_lines[0] + " " + word
                dialog_object[0] = my_font.render(dialog_lines[0], True, white)
                print(dialog_lines[0])
                screen.blit(dialog_object[0], dialog_rects[0])
                pygame.display.update()
                time.sleep(.1)
            elif my_font.size(dialog_lines[1] + " " + word)[0] < dialog_box.width - 20:
                dialog_lines[1] = dialog_lines[1] + " " + word
                dialog_object[1] = my_font.render(dialog_lines[0], True, white)
                screen.blit(dialog_object[1], dialog_rects[1])
                pygame.display.update()
                time.sleep(.1)

        # height = dialog_rects[0].height
        # for i, line in enumerate(dialog_object):
        #     screen.blit(line, ((dialog_box.x + 10), height * i))
        pygame.display.update()