#!/usr/bin/env python
# coding: utf-8

# Created 2012-09-21

import pygame, sys
from pygame.locals import *
#import pdb
#pdb.set_trace()

SCREEN_X = 1024
SCREEN_Y = 768

pygame.init()
screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y), HWSURFACE|DOUBLEBUF)
clock = pygame.time.Clock()
if not pygame.joystick.get_init():
    print("Joystick not found")
    sys.exit(255)

jid = pygame.joystick.get_count()
if jid == 0:
    print("Joystick not found")
    sys.exit(255)

joy = pygame.joystick.Joystick(jid - 1)
joy.init()

while True:
    for event in pygame.event.get():
        if event.type == JOYAXISMOTION:
            print("axis = %d, val = %f" % (event.axis, event.value))
    clock.tick(50)
