#!/usr/bin/env python
# coding: utf-8

# Created 2012-09-21
# © Copyright 2012 OllyCat. All Rights Reserved.

import pygame, sys
from pygame.locals import *
#import pdb
#pdb.set_trace()

SCREEN_X = 1024
SCREEN_Y = 768

pygame.init()
screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y), HWSURFACE|DOUBLEBUF)
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit(0)
    clock.tick(50)
