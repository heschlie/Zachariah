#!/usr/bin/env python
# Written by alex@nyrpnz.com March 14 2012
"Event echoer in Pygame."
 
import pygame
from pygame.locals import *
 
def main():
        "Opens a window and prints events to the terminal. Closes on ESC or QUIT."
        pygame.init()
        screen = pygame.display.set_mode((640, 480))
        pygame.display.set_caption("JOYTEST")
        clock = pygame.time.Clock()
        joysticks = []
        for i in range(0, pygame.joystick.get_count()):
            joysticks.append(pygame.joystick.Joystick(i))
            joysticks[-1].init()
            print "Detected joystick '",joysticks[-1].get_name(),"'"
            print joysticks[i].get_numhats()
        while 1:
                clock.tick(60)
                print joysticks[0].get_hat(0)

                for event in pygame.event.get():
                        if event.type == QUIT:
                                print "Received event 'Quit', exiting."
                                return
                        elif event.type == KEYDOWN and event.key == K_ESCAPE:
                                print "Escape key pressed, exiting."
                                return
                        elif event.type == KEYDOWN:
                                print "Keydown,",event.key
                        elif event.type == KEYUP:
                                print "Keyup,",event.key
                        elif event.type == MOUSEMOTION:
                                print "Mouse movement detected."
                        elif event.type == MOUSEBUTTONDOWN:
                                print "Mouse button",event.button,"down at",pygame.mouse.get_pos()
                        elif event.type == MOUSEBUTTONUP:
                                print "Mouse button",event.button,"up at",pygame.mouse.get_pos()
                        elif event.type == JOYAXISMOTION:
                                print "Joystick '",joysticks[event.joy].get_name(),"' axis",event.axis,"motion."
                        elif event.type == JOYBUTTONDOWN:
                                print "Joystick '",joysticks[event.joy].get_name(),"' button",event.button,"down."
                        elif event.type == JOYBUTTONUP:
                                print "Joystick '",joysticks[event.joy].get_name(),"' button",event.button,"up."
                        elif event.type == JOYHATMOTION:
                                print "Joystick '",joysticks[event.joy].get_name(),"' hat",event.hat," moved.", event.value

if __name__ == "__main__":
        main()