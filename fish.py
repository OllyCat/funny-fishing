#!/usr/bin/env python
# coding: utf-8

# Created 2012-09-18
"""
Содержит класс рыб. Сначала загружается просто картинка, в перспективе планирую
добавить анимацию.
"""

import pygame, random

class Fish():
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
        # сохраняем имя файла рыбы
        self.name = img_name
        # создаем базовую картинку рыбы с альфа каналом
        self.base_img = pygame.image.load(self.name).convert_alpha()
        # сохраняем ее размеры
        self.x_size, self.y_size = self.base_img.get_size()

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

        # ставим ей случайную скорость
        self.speed = random.randint(1, 5)

        # если направление реверсное (self.direction = 1) то изменяем начальное
        # положение на "за правый край экрана" и отражаем рыбу по вертикали а
        # так же задаем отрицательную скорость
        if self.direction:
            # устанавливаем рыбу в начальное положение: за правый край экрана
            self.x_pos = 1024
            # задаем отрицательную скорость
            self.speed = 0 - self.speed
            self.img = pygame.transform.flip(self.img, True, False)
        # иначе - рыбу за левый край и скорость оставляем положительную
        else:
            # устанавливаем рыбу в начальное положение: за левый край экрана
            self.x_pos = 0 - self.x_size

        # устанавливаем рыбу в начальное положение: в случайную позицию по высоте
        self.y_pos = random.randint(0, 768 - self.y_size)

        # отрисовка случайной буквы на середину копии
        self.img.blit(text, (self.x_size/2 - text.get_width()/2, self.y_size/2 - text.get_height()/2))

    '''
    получаем координаты мыши и флаг catch. если он равен букве на рыбе - значит рыба будет
    поймана, если крючок находится в ее области
    возвращаем True если рыба попалась
    '''
    def update(self, x, y, catch):
        #import pdb
        #pdb.set_trace()
        # код возврата
        ret = False

        # проверяем: если флаг поимки не False и при этом курсор мыши попадает на рыбу...
        if(catch and (self.x_pos < x < (self.x_size + self.x_pos)) and (self.y_pos < y < (self.y_size + self.y_pos))):
            # а так же пиксель под курсором не прозрачный...
            if((self.img.get_at((x - self.x_pos, y - self.y_pos)).a > 200) and catch == self.rnd_char):
                # то возвращаем True (поймали) и переинициализируем рыбу заново
                ret = True
                self.init_fish()
            else:
                # если же флаг поимки стоял, но условия попадения крючка не совпали - "мазила"! :)
                print "Мазила!"
        # сдвигаем рыбу
        self.x_pos += self.speed

        # если рыба ушла за край экрана - переинициализируем ее
        if (self.x_pos > 1024 and self.speed > 0) or (self.x_pos < (0 - self.x_size) and self.speed < 0):
            self.init_fish()

        # в конце отрисовываем рыбу на экране
        self.screen.blit(self.img, (self.x_pos, self.y_pos))
        # и вернем код возврата
        return ret
