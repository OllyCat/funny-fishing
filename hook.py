#!/usr/bin/env python
# coding: utf-8

# Created 2012-09-18
"""
Класс содержит обработку удочки. Пока просто отрисовку крючка, поплавка и
лески. В будущем, надеюсь, обработку аппаратной удочки сделать.
"""

import os
import pygame

class FishHook():
	# Конструктор получает screen
    def __init__(self, scr):
        self.screen = scr
        # загружаем изображение крючка
        self.hook_img = pygame.image.load(os.path.join("data", "hook.png")).convert_alpha()
        # находим его середину, что бы можно было его позиционировать на центр мыши
        self.x_delta = self.hook_img.get_width() / 2
        self.y_delta = self.hook_img.get_height() / 2

	# получаем координаты мыши
    def update(self, x, y):
        # делаем курсор мыши невидимым
        pygame.mouse.set_visible(False)
        # рисуем леску
        pygame.draw.line(self.screen, (0, 0, 0), (x, y - self.y_delta), (x, 0))
        # рисуем крючок
        self.screen.blit(self.hook_img, (x - self.x_delta, y - self.y_delta))
