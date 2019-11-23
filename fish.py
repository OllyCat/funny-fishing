#!/usr/bin/env python
# coding: utf-8

# Created 2012-09-18
"""
Содержит класс рыб. Сначала загружается просто картинка, в перспективе планирую
добавить анимацию.
"""

import pygame
import random


class Fish:
    '''
        Конструктор получает surface и путь к изображению рыбы
        screen - хранит объект screen
        img - хранит спрайт рыбы
        x_pos, y_pos - стартовая позиция
        speed - случайная скорость рыбы
        ubar - хранит объект бара, для получения текущей буквы
    '''
    def __init__(self, scr, rect, img_name, cur_char, ubar):
        # сохраняем бар
        self.u_bar = ubar
        # сохраняем экран
        self.screen = scr
        # сохраняем имя файла рыбы
        self.name = img_name
        # создаем базовую картинку рыбы с альфа каналом
        self.image = pygame.image.load(self.name).convert_alpha()
        # сохраняем ее Rect
        self.rect = self.image.get_rect()
        # сохраняем букву, за которой охотимся
        self.cur_char = self.u_bar.get_curchar()

        # алфавит
        # установка случайной буквы на рыбу
        self.alpabet = u"АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"

        # сохраняем Rect области куда можно рисовать
        self.work_rect = rect

        # получаем фонт
        fonts = pygame.font.match_font('Vendetta,Arial')
        self.font = pygame.font.Font(fonts, 65)

        # инициализируем рыбу
        self.init_fish()

    # инициализация рыбы: установка стартовой позиции и буквы
    def init_fish(self):
        # установка случайной буквы на рыбу
        # берем букву из бара, что бы не было сильных отклонений
        self.cur_char = self.u_bar.get_curchar()
        self.set_rndchar()

        # ставим случайным образом направление движения рыбы
        self.direction = random.randint(0, 1)

        # отрисовка текста
        text = self.font.render(self.rnd_char, 1, (255, 255, 255))
        # копия рыбы
        self.img = self.image.copy()
        self.rect = self.img.get_rect()

        # ставим ей случайную скорость
        self.speed = random.randint(1, 5)

        # если направление реверсное (self.direction = 1) то изменяем начальное
        # положение на "за правый край экрана" и отражаем рыбу по вертикали а
        # так же задаем отрицательную скорость
        if self.direction:
            # устанавливаем рыбу в начальное положение: за правый край экрана
            self.rect.x = self.work_rect.x + self.work_rect.w
            # задаем отрицательную скорость
            self.speed = 0 - self.speed
            self.img = pygame.transform.flip(self.img, True, False)
        # иначе - рыбу за левый край и скорость оставляем положительную
        else:
            # устанавливаем рыбу в начальное положение: за левый край экрана
            self.rect.x = -self.rect.w

        # устанавливаем рыбу в начальное положение: в случайную позицию по высоте
        self.rect.y = random.randint(self.work_rect.y, self.work_rect.y + self.work_rect.h - self.rect.h)

        # отрисовка случайной буквы на середину копии
        self.img.blit(text, (self.rect.w / 2 - text.get_width() / 2, self.rect.h / 2 - text.get_height() / 2))

    '''
    получаем координаты мыши и флаг catch. если он равен букве на рыбе - значит рыба будет
    поймана, если крючок находится в ее области
    возвращаем True если рыба попалась
    '''
    def update(self, x, y):
        # сдвигаем рыбу
        self.rect.x += self.speed

        # если рыба ушла за край экрана - переинициализируем ее
        if (self.rect.x > (self.work_rect.x + self.work_rect.w) and self.speed > 0) or (self.rect.x < -self.rect.w and self.speed < 0):
            self.init_fish()

        # в конце отрисовываем рыбу на экране
        self.draw()

    def draw(self):
        self.screen.blit(self.img, self.rect)

    def get_char(self):
        return self.rnd_char

    def set_reverse(self):
        self.speed = -self.speed * 5
        self.img = pygame.transform.flip(self.img, True, False)

    def set_rndchar(self):
        cur_idx = self.alpabet.index(self.cur_char)
        min_idx = cur_idx - 2
        max_idx = cur_idx + 2
        rnd_idx = random.randint(min_idx, max_idx)
        if rnd_idx >= len(self.alpabet):
            rnd_idx = rnd_idx - len(self.alpabet)
        self.rnd_char = self.alpabet[rnd_idx]

    def show_fish(self):
        pass
