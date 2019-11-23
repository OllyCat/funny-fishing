#!/usr/bin/env python
# coding: utf-8

# Created 2012-09-21
# использует девелоперскую часть кода pygame для камары

import sys
import pygame, pygame.camera
from pygame.locals import *
#import pdb
#pdb.set_trace()

size = SCREEN_X, SCREEN_Y = (640, 480)

pygame.init()
pygame.camera.init()
screen = pygame.display.set_mode(size, HWSURFACE|DOUBLEBUF)
clock = pygame.time.Clock()

cameras = pygame.camera.list_cameras()

if not cameras:
    print("Camera not found.")
    sys.exit(255)

camera = pygame.camera.Camera(cameras[0], size, "RGB")
camera.start()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit(0)
    if camera.query_image():
        frame = camera.get_image()
        screen.blit(frame, (0,0))

    crect = pygame.draw.rect(screen, (255,0,0), (145,105,30,30), 4)

    pygame.display.update()
    clock.tick(25)
