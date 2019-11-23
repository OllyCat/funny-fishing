#!/usr/bin/env python
# coding: utf-8

# Created 2012-09-18
"""
Класс содержит отрисовку моря и в последствии различные мелочи: камни,
крабов водоросли на дне и так далее. Пока это заглушка.
"""

import pygame
import os


class Sea():

    def __init__(self, scr, rect):
        # сохраняем экран
        self.screen = scr
        # имя файла фона (пока это просто градиент)
        back_file = os.path.join("data", "background.png")

        # загружаем фон (а надо ли альфа канал? может потом надо будет)
        self.image = pygame.image.load(back_file).convert_alpha()
        self.rect = self.image.get_rect()

        # сохраняем область для рисования
        self.work_rect = rect

    # рисуем это все на экране :)
    def update(self):
        self.screen.set_clip(self.work_rect)
        self.screen.blit(self.image, self.rect)
