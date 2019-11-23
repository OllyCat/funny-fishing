#!/usr/bin/env python
# coding: utf-8

# Created 2012-09-21
# использует opencv

import sys
import pygame, cv
import numpy as np
from pygame.locals import *
#import pdb
#pdb.set_trace()

size = SCREEN_X, SCREEN_Y = (640, 480)

pygame.init()
screen = pygame.display.set_mode(size, HWSURFACE|DOUBLEBUF)
clock = pygame.time.Clock()
fonts = pygame.font.match_font('Vendetta,Arial')
font = pygame.font.Font(fonts, 10)
text_color = (0x80,0xff,0x80)

#cameras = pygame.camera.list_cameras()
#
#if not cameras:
#    print("Camera not found.")
#    sys.exit(255)

camera = cv.CaptureFromCAM(0)
print camera
frame = cv.QueryFrame(camera)
print frame
#cv.CvtColor(frame, frame, cv.CV_BGR2HSV)
frameTH = cv.CreateImage(cv.GetSize(frame), 8, 1)

original = False
th_lower, th_upper = 45, 50

while True:
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            sys.exit(0)
        if event.type == KEYDOWN and event.key == K_UP:
            th_upper += 1
            if th_upper > 255: th_upper = 255
        if event.type == KEYDOWN and event.key == K_DOWN:
            th_upper -= 1
            if th_upper < 0: th_upper = 0
        if event.type == KEYDOWN and event.key == K_RIGHT:
            th_lower += 1
            if th_lower > 255: th_lower = 255
        if event.type == KEYDOWN and event.key == K_LEFT:
            th_lower -= 1
            if th_lower < 0: th_lower = 0
        if event.type == KEYDOWN and event.key == K_RETURN:
            original = not original
        #if event.type == MOUSEMOTION:
        #    mouse = event.pos
        #if event.type == MOUSEBUTTONDOWN and event.button == 1:
        #    cv.FloodFill(im, mouse, (0,0,255), cv.ScalarAll(10), cv.ScalarAll(20), cv.CV_FLOODFILL_FIXED_RANGE)

    frame = cv.QueryFrame(camera)
    frame_final = cv.CloneImage(frame)

    #cv.CvtColor(frame, frameMask, cv.CV_BGR2HSV)
    #cv.InRangeS(frameMask, cv.Scalar(16, 73, 50), cv.Scalar(16, 73, 100), frameTH)
    #cv.SaveImage("test.jpg", frameTH)

    cv.Smooth(frame, frame, cv.CV_GAUSSIAN, 3, 3)
    cv.CvtColor(frame, frameTH, cv.CV_BGR2GRAY)
    cv.Canny(frameTH, frameTH, th_lower, th_upper)
    cv.CvtColor(frameTH, frame_final, cv.CV_GRAY2RGB)
    frame_surface = pygame.image.fromstring(frame_final.tostring(), cv.GetSize(frame_final), "RGB")

    #cv.CvtColor(frame, frame, cv.CV_BGR2RGB)
    #frame_surface = pygame.image.fromstring(frame.tostring(), cv.GetSize(frame), "RGB")

    frame_surface = pygame.transform.flip(frame_surface, True, False)
    screen.blit(frame_surface, (0,0))

    text = font.render("Lower threshhold = " + str(th_lower), 1, text_color)
    screen.blit(text, (5,5))
    text = font.render("Upper threshhold = " + str(th_upper), 1, text_color)
    screen.blit(text, (5,15))

    #crect = pygame.draw.rect(screen, (255,0,0), (145,105,30,30), 4)

    pygame.display.update()
    clock.tick(60)
