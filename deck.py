#!/usr/bin/env python
# coding: utf-8
# VIM: tabstop=4 expandtab shiftwidth=4 softtabstop=4

# Created 2019-11-23

class Deck():
    '''
    Класс набора данных, колода.
    Изначально использовался алфавит и необходимости в этом классе не было.
    Для реализации слогов, вместо букв, требуется рефакторинг и отжельный класс.
    '''
    def __init__(self):
        # наобр данных
        self.deck = list('АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ')

    '''
    получить всю колоду
    '''
    def get_all(self):
        return self.deck
