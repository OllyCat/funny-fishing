#!/usr/bin/env python
# coding: utf-8

# Created 2012-09-21
# использует opencv (cv2)

import sys
import pygame
import cv2
import numpy as np
from pygame.locals import *

#import pdb
#pdb.set_trace()

size = SCREEN_X, SCREEN_Y = (640, 480)

pygame.init()
screen = pygame.display.set_mode(size, HWSURFACE | DOUBLEBUF)
clock = pygame.time.Clock()
fonts = pygame.font.match_font('Vendetta,Arial')
font = pygame.font.Font(fonts, 10)
text_color = (0x80, 0xff, 0x80)

camera = cv2.VideoCapture(0)

original = 0
key_state = (None, None)
th_lower, th_upper = 127, 255

while True:
    for event in pygame.event.get():
        if event.type == QUIT or \
          (event.type == KEYDOWN and \
           event.key == K_ESCAPE):
            sys.exit(0)
        if event.type == KEYDOWN and event.key == K_RETURN:
            original += 1
            #original = original % 3
        if event.type == KEYDOWN:
            key_state = (event.type, event.key)
        if event.type == MOUSEMOTION:
            mouse = event.pos
        if event.type == KEYUP:
            key_state = (None, None)
        #if event.type == MOUSEBUTTONDOWN and event.button == 1:
        #    cv.FloodFill(im, mouse, (0,0,255), cv.ScalarAll(10), cv.ScalarAll(20), cv.CV_FLOODFILL_FIXED_RANGE)

    if key_state:
        if event.type == KEYDOWN and event.key == K_UP:
            th_upper += 1
            if th_upper > 255:
                th_upper = 255
        if event.type == KEYDOWN and event.key == K_DOWN:
            th_upper -= 1
            if th_upper < 0:
                th_upper = 0
        if event.type == KEYDOWN and event.key == K_RIGHT:
            th_lower += 1
            if th_lower > 255:
                th_lower = 255
        if event.type == KEYDOWN and event.key == K_LEFT:
            th_lower -= 1
            if th_lower < 0:
                th_lower = 0

    err, frame = camera.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    #frameTH = cv2.split(frame)[original]

    frameTH = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    err, frameTH = cv2.threshold(frameTH, th_lower, th_upper, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    fg = cv2.erode(frameTH, None, iterations = 2)
    bgt = cv2.dilate(frameTH, None, iterations = 3)
    err, bg = cv2.threshold(bgt, 1, 128, 1)
    marker = cv2.add(fg, bg)
    marker32 = np.int32(marker)
    cv2.watershed(frame, marker32)
    m = cv2.convertScaleAbs(marker32)
    err, frameTH = cv2.threshold(m, th_lower, th_upper, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    frame = cv2.bitwise_and(frame, frame, mask = frameTH)

    #frame = cv2.cvtColor(frameTH, cv2.COLOR_GRAY2RGB)

    frame_surface = pygame.image.fromstring(frame.tostring(), (frame.shape[1], frame.shape[0]), "RGB")

    frame_surface = pygame.transform.flip(frame_surface, True, False)
    screen.blit(frame_surface, (0, 0))

    text = font.render("Lower threshhold = " + str(th_lower), 1, text_color)
    screen.blit(text, (5, 5))
    text = font.render("Upper threshhold = " + str(th_upper), 1, text_color)
    screen.blit(text, (5, 15))

    #crect = pygame.draw.rect(screen, (255,0,0), (145,105,30,30), 4)

    pygame.display.update()
    clock.tick(60)
