import pygame
from pygame.locals import *
import time


def start_dialog(text, screen):
    paragraph = text.split()
    screen_size = screen.get_size()
    my_font = pygame.font.Font('Fonts/Sansation_Regular.ttf', 24)
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

    screen.fill((0, 0, 0), dialog_box)
    #pygame.draw.rect(screen, (0, 0, 0), dialog_box)

    delay = .1
    for word in paragraph:
        if get_keys():
            delay = 0
        if my_font.size(dialog_lines[0] + " " + word)[0] < dialog_box.width - 20:
            dialog_lines[0] = dialog_lines[0] + " " + word
            dialog_object[0] = my_font.render(dialog_lines[0], True, white)
            screen.blit(dialog_object[0], dialog_rects[0])
            pygame.display.update()
            time.sleep(delay)
        elif my_font.size(dialog_lines[1] + " " + word)[0] < dialog_box.width - 20:
            dialog_lines[1] = dialog_lines[1] + " " + word
            dialog_object[1] = my_font.render(dialog_lines[1], True, white)
            screen.blit(dialog_object[1], dialog_rects[1])
            pygame.display.update()
            time.sleep(delay)
        elif my_font.size(dialog_lines[2] + " " + word)[0] < dialog_box.width - 20:
            dialog_lines[2] = dialog_lines[2] + " " + word
            dialog_object[2] = my_font.render(dialog_lines[2], True, white)
            screen.blit(dialog_object[2], dialog_rects[2])
            pygame.display.update()
            time.sleep(delay)
        elif my_font.size(dialog_lines[3] + " " + word)[0] < dialog_box.width - 20:
            dialog_lines[3] = dialog_lines[3] + " " + word
            dialog_object[3] = my_font.render(dialog_lines[3], True, white)
            screen.blit(dialog_object[3], dialog_rects[3])
            pygame.display.update()
            time.sleep(delay)
        elif my_font.size(dialog_lines[4] + " " + word)[0] < dialog_box.width - 20:
            dialog_lines[4] = dialog_lines[4] + " " + word
            dialog_object[4] = my_font.render(dialog_lines[4], True, white)
            screen.blit(dialog_object[4], dialog_rects[4])
            pygame.display.update()
            time.sleep(delay)
        elif my_font.size(dialog_lines[4] + " " + word)[0] > dialog_box.width - 20:
            pygame.event.clear()
            wait = True
            while wait:
                if get_keys():
                    wait = False
                    dialog_lines[:] = []
                    dialog_lines = ['', '', '', '', '']
                    pygame.draw.rect(screen, (0, 0, 0), dialog_box)
                    pygame.event.clear()
                    delay = .1
    cont = False
    pygame.event.clear()
    while not cont:
        if get_keys():
            cont = True


def get_keys():
    for event in pygame.event.get():
        if event.type == KEYUP:
            if event.key == K_SPACE or \
                    event.key == K_RETURN:
                return True
        elif event.type == JOYBUTTONUP:
            if event.button == 0 or \
                    event.button == 1:
                return True
        else:
            return False