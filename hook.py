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
        # сохраняем Rect
        self.hook_img_rect = self.hook_img.get_rect()

        self.draw()

	# получаем координаты мыши в виде тюпла
    def update(self, pos):
        # делаем курсор мыши невидимым
        pygame.mouse.set_visible(False)
        # меняем позицию крючка
        delt_pos = (pos[0] - self.hook_img_rect.x, pos[1] - self.hook_img_rect.y)
        self.hook_img_rect.move_ip(delt_pos)
        # рисуем леску
        pygame.draw.line(self.screen, (0, 0, 0), (pos[0] + self.hook_img_rect.w/2, pos[1]), (pos[0] + self.hook_img_rect.w/2, 0))
        # рисуем крючок
        self.draw()

    def draw(self):
        self.screen.blit(self.hook_img, self.hook_img_rect)

    def get_rect(self):
        return self.hook_img_rect
