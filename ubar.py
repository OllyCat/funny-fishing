#!/usr/bin/env python
# coding: utf-8

# Created 2012-09-22

import os
import pygame
import random


class UBar():
    '''
    класс отрисовки верхнего бара:
    [буква подсказка] |||шкала пойманных рыб|||
    так же тут выставляется текущая буква, за которой идет охота
    '''
    def __init__(self, screen, rect, deck):
        # цвет фонтов
        self.f_color = (0xff, 0xff, 0xff)
        self.screen = screen
        # сохраняем Rect области бара
        self.rect = rect
        # массив данных для ловли
        self.chars = deck.get_all()
        # счетчик пойманных рыб
        self.fish_counter = 0
        # указатель текущей буквы
        self.char_counter = 0

        self.image = pygame.image.load(os.path.join("data", "pano.png")).convert()

        fonts = pygame.font.match_font('Vendetta,Arial')
        self.font = pygame.font.Font(fonts, 24)

    '''
    функция возвращает текущую букву, которую ловим
    '''
    def get_curchar(self):
        if len(self.chars) > 0:
            return self.chars[self.char_counter]
        return 'Файл deck.txt не найден или пуст!'

    '''
    функция обновления класса
    получает флаг, что рыба поймана
    '''
    def update(self, catch):
        # если поймана рыба то
        if catch:
            # увеличиваем счетчик пойманных рыб
            self.fish_counter += 1
            # если счетчик переполнился, то
            if self.fish_counter >= 3:
                # сбрасываем его
                self.fish_counter = 0
                # устанавливаем счетчик случайным образом
                self.char_counter = random.randrange(0, len(self.chars) - 1)
                # увеличиваем указатель буквы в массиве букв
                #self.char_counter += 1
                # если счетчик указателя переполнился, то
                #if self.char_counter >= len(self.chars):
                #    # обнуляем его
                #    self.char_counter = 0
        self.draw()

    def draw(self):
        # устанавливаем область бара
        self.screen.set_clip(self.rect)
        # получаем текущий элемент, либо сообщение об ошибке
        c = self.get_curchar()
        # получаем surface текста
        text = self.font.render(c, 1, self.f_color)
        # получаем rect текста
        text_rect = text.get_rect()
        # если текст длинный (сообщение об ошибке) умещаем его в экран
        if len(c) > 10:
            text_rect.fit(self.rect)
        else:
            # если нет - центруем
            text_rect.centerx = self.rect.h / 2

        # центруем по вертикали
        text_rect.centery = text_rect.centery + (self.rect.h - text_rect.h) / 2
        # отрисовываем текст
        self.screen.blit(self.image, (0, 0))
        self.screen.blit(text, text_rect)
        # отрисовываем бары пойманных рыб
        for i in range(self.fish_counter):
            pygame.draw.rect(self.screen, self.f_color, (80 + i * 10, 14, 5, 14))

