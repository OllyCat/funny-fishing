#!/usr/bin/env python
# coding: utf-8

# Created 2012-09-23

import sys, os
import pygame
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((1024, 768), HWSURFACE|DOUBLEBUF)
clock = pygame.time.Clock()

img = pygame.image.load("data/fish01.png").convert_alpha()
img_rect = img.get_rect()
speed_x = 1
speed_y = 1
img_rect.x = 100
img_rect.y = 100

sound = pygame.mixer.Sound("sound/fail_char.wav")
if not sound:
    sys.exit(255)

sound.play()

while True:
    screen.fill((0,0,0))
    screen.blit(img, img_rect)
    pygame.display.update()
    clock.tick(50)

    if (img_rect.x > (1024 - img_rect.w)) or (img_rect.x < 0):
        speed_x = -speed_x
    if (img_rect.y > (768 - img_rect.h)) or (img_rect.y < 0):
        speed_y = -speed_y

    img_rect.move_ip(speed_x, speed_y)
    print img_rect.centerx
