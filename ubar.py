#!/usr/bin/env python
# coding: utf-8

# Created 2012-09-22

import os
import pygame

class UBar():
    '''
    класс отрисовки верхнего бара:
    [буква подсказка] |||шкала пойманных рыб|||
    так же тут выставляется текущая буква, за которой идет охота
    '''
    def __init__(self, screen, rect):
        self.screen = screen
        # сохраняем Rect области бара
        self.rect = rect
        # массив букв для ловли
        self.chars = u'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
        # счетчик пойманных рыб
        self.fish_counter = 0
        # указатель текущей буквы
        self.char_counter = 0

        self.image = pygame.image.load(os.path.join("data", "pano.png")).convert()

        fonts = pygame.font.match_font('Vendetta,Arial')
        self.font = pygame.font.Font(fonts, 42)

    '''
    функция возвращает текущую букву, которую ловим
    '''
    def get_curchar(self):
        return self.chars[self.char_counter]

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
            if self.fish_counter >= 10:
                # сбрасываем его
                self.fish_counter = 0
                # увеличиваем указатель буквы в массиве букв
                self.char_counter += 1
                # если счетчик указателя переполнился, то
                if self.char_counter >= len(self.chars):
                    # обнуляем его
                    self.char_counter = 0
        self.draw()

    def draw(self):
        self.screen.set_clip(self.rect)
        text = self.font.render(self.get_curchar(), 1, (0x00,0x80,0x00))
        text_rect = text.get_rect()
        text_rect.centerx = text_rect.centery = text_rect.centery + (self.rect.h - text_rect.h)/2
        self.screen.blit(self.image, (0, 0))
        self.screen.blit(text, text_rect)
        for i in xrange(self.fish_counter):
            pygame.draw.rect(self.screen, (0x00, 0x80, 0x00), (80 + i * 10, 14, 5 , 14))
        pass
