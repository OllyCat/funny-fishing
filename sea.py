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

    def __init__(self, scr):
        # сохраняем экран
        self.screen = scr
        # имя файла фона (пока это просто градиент)
        back_file = os.path.join("data", "background.png")
        # позиция бакграунда (пока не знаю надо ли)
        self.draw_pos = (0, 0)
        # загружаем фон (а надо ли альфа канал? может потом надо будет)
        self.background = pygame.image.load(back_file).convert_alpha()

	# рисуем это все на экране :)
    def update(self):
        self.screen.blit(self.background, self.draw_pos)
        return
