#!/usr/bin/env python
# coding: utf-8

# Created 2012-09-18
"""
Содержит класс рыб. Сначала загружается просто картинка, в перспективе планирую
добавить анимацию.
"""

import pygame, random

class Fish:
    '''
        Конструктор получает surface и путь к изображению рыбы
        screen - хранит объект screen
        img - хранит спрайт рыбы
        x_pos, y_pos - стартовая позиция
        speed - случайная скорость рыбы
    '''
    def __init__(self, scr, img_name):
        # сохраняем экран
        self.screen = scr
        self.SCREEN_X, self.SCREEN_Y = self.screen.get_size()
        # сохраняем имя файла рыбы
        self.name = img_name
        # создаем базовую картинку рыбы с альфа каналом
        self.base_img = pygame.image.load(self.name).convert_alpha()
        # сохраняем ее Rect
        self.base_img_rect = self.base_img.get_rect()

        # получаем фонт
        fonts = pygame.font.match_font('Vendetta,Arial')
        self.font = pygame.font.Font(fonts, 65)

        # инициализируем рыбу
        self.init_fish()

    # инициализация рыбы: установка стартовой позиции и буквы
    def init_fish(self):
        # алфавит
        alpabet = u"АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
        # установка случайной буквы на рыбу
        #self.rnd_char = alpabet[random.randint(0, len(alpabet) - 1)]
        self.rnd_char = alpabet[random.randint(0, 3)]

        # ставим случайным образом направление движения рыбы
        self.direction = random.randint(0, 1)

        # отрисовка текста
        text = self.font.render(self.rnd_char, 1, (255,255,255))
        # копия рыбы
        self.img = self.base_img.copy()
        self.img_rect = self.img.get_rect()

        # ставим ей случайную скорость
        self.speed = random.randint(1, 5)

        # если направление реверсное (self.direction = 1) то изменяем начальное
        # положение на "за правый край экрана" и отражаем рыбу по вертикали а
        # так же задаем отрицательную скорость
        if self.direction:
            # устанавливаем рыбу в начальное положение: за правый край экрана
            self.img_rect.x = self.SCREEN_X
            # задаем отрицательную скорость
            self.speed = 0 - self.speed
            self.img = pygame.transform.flip(self.img, True, False)
        # иначе - рыбу за левый край и скорость оставляем положительную
        else:
            # устанавливаем рыбу в начальное положение: за левый край экрана
            self.img_rect.x = -self.img_rect.w

        # устанавливаем рыбу в начальное положение: в случайную позицию по высоте
        self.img_rect.y = random.randint(0, self.SCREEN_Y - self.img_rect.h)

        # отрисовка случайной буквы на середину копии
        self.img.blit(text, (self.img_rect.w/2 - text.get_width()/2, self.img_rect.h/2 - text.get_height()/2))

    '''
    получаем координаты мыши и флаг catch. если он равен букве на рыбе - значит рыба будет
    поймана, если крючок находится в ее области
    возвращаем True если рыба попалась
    '''
    def update(self, x, y): #, catch):
        # сдвигаем рыбу
        self.img_rect.x += self.speed

        # если рыба ушла за край экрана - переинициализируем ее
        if (self.img_rect.x > self.SCREEN_X and self.speed > 0) or (self.img_rect.x < (0 - self.img_rect.w) and self.speed < 0):
            self.init_fish()

        # в конце отрисовываем рыбу на экране
        self.draw()

    def draw(self):
        self.screen.blit(self.img, self.img_rect)

    def get_rect(self):
        return self.img_rect

    def get_char(self):
        return self.rnd_char

    def set_reverse(self):
        self.speed = -self.speed * 3
        self.img = pygame.transform.flip(self.img, True, False)

    def show_fish(self):
        pass
