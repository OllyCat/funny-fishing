#!/usr/bin/env python
# coding: utf-8

# Created 2012-09-18

"""
Основной скрипт. Содержит инициализации окна, классов и основную петлю с
обработкой событий.
"""

import pygame
import sys
import random
import math
import os
import re
from pygame.locals import *

import deck
import sea
import fish
import hook
import ubar
import sound


class Game:
    def __init__(self):
        # базовые размеры экрана, бара и "моря"
        self.SCREEN_RECT = pygame.Rect((0, 0), (1024, 768))
        self.BAR_RECT    = pygame.Rect((0, 0), (self.SCREEN_RECT.w, 60))
        self.SEA_RECT    = pygame.Rect((0, self.BAR_RECT.h), (self.SCREEN_RECT.w, self.SCREEN_RECT.h - self.BAR_RECT.h))

        # инициализация pygame
        pygame.init()
        # устанавливаем заголовок
        pygame.display.set_caption("Весёлая рыбалка")
        # создаем окно
        self.screen = pygame.display.set_mode((self.SCREEN_RECT.w, self.SCREEN_RECT.h), HWSURFACE | DOUBLEBUF)

        # массив рыб
        self.fishes = []
        # заполняем список файлов рыб
        data_dir = os.listdir("data")
        # выбираем только файлы рыб
        self.fish_pics = re.findall("fish\d\d.png", ''.join(data_dir))
        if len(self.fish_pics) == 0:
            print("Error! Fish pics not found!")
            sys.exit(255)

        # создаём колоду
        self.deck = deck.Deck()

        # создаем верхний бар
        self.u_bar = ubar.UBar(self.screen, self.BAR_RECT, self.deck)
        self.u_bar.draw()

        # загружаем звуки
        self.games_sounds = sound.Sound()
        # включаем музыку
        self.games_sounds.play_music()

        # буква за которой охотимся
        self.big_char = self.u_bar.get_curchar()

        # создаем море
        self.Sea = sea.Sea(self.screen, self.SEA_RECT)

        # создаем крючок и леску
        self.FishHook = hook.FishHook(self.screen, self.SEA_RECT)

        # таймер
        self.clock = pygame.time.Clock()

        # инициализируем джойстик, если есть
        if pygame.joystick.get_count() > 0:
            joy = pygame.joystick.Joystick(0)
            joy.init()

        # заполняем массив рыбами передавая путь до файлов
        for i in range(3):
            self.fishes.append(fish.Fish(self.screen, self.SEA_RECT, os.path.join("data", random.choice(self.fish_pics)), self.big_char, self.u_bar, self.deck))

    def run(self):
        # попросим поймать начальную букву
        self.games_sounds.play_startchar(self.big_char)

        # обновляем крючок
        self.FishHook.update(pygame.mouse.get_pos())

        # получаем позицию мыши
        self.x, self.y = pygame.mouse.get_pos()

        # основной цикл
        while True:
            # устанавливаем флаг поимки в False
            self.catch = False

            # опрос очереди событий
            self.check_events()

            # прорисовываем море
            self.Sea.update()

            # в цикле обновляем всех рыб
            for j in self.fishes.__reversed__():
                # рыбе передаем позицию курсора и флаг поимки, получаем False, если не поймана, или True, если поймана
                ret = j.update(self.x, self.y)

            # обновляем крючок и леску
            self.FishHook.update((self.x, self.y))

            # обновляем дисплей
            pygame.display.update()

            # обнаруживаем пересечение объектов, если при этом стоит флаг поимки и
            # буква рыбы совпадает с искомой буквой, то рыба поймана, если не
            # совпадает - то не поймана и разворачивается
            fish_index = self.FishHook.rect.collidelist(list(map(lambda x: x.rect, self.fishes)))
            if self.catch and fish_index >= 0:
                if self.fishes[fish_index].get_char() == self.catch:
                    self.u_bar.update(self.catch)
                    self.catch = False
                    new_char = self.u_bar.get_curchar()
                    self.fishes[fish_index].show_fish()
                    cached_fish = self.fishes.pop(fish_index)
                    self.games_sounds.play_success(self.big_char)
                    self.catch_success()
                    self.fishes.append(fish.Fish(self.screen, self.SEA_RECT, os.path.join("data", random.choice(self.fish_pics)), self.big_char, self.u_bar, self.deck))
                    if new_char != self.big_char:
                        self.big_char = new_char
                        self.games_sounds.play_startchar(self.big_char)
                else:
                    self.fishes[fish_index].set_reverse()
                    self.catch_fail(fish_index)

            # отсчитываем тики для задержки
            self.clock.tick(50)
        return

    def catch_success(self):
        self.screen.set_clip()

        # количество шагов приближения картинки
        fps = 30
        # загружаем картинку
        base_thumb = pygame.image.load(os.path.join("data", "thumbs_up.png")).convert_alpha()
        # получаем размеры экрана, на котором рисуем и размер картинки
        screen_rect = self.screen.get_rect()
        base_thumb_rect = base_thumb.get_rect()
        base_thumb_rect.center = screen_rect.center
        # шаг увеличения картинки
        step = int(base_thumb_rect.h / fps)
        # сохраним кусок экрана для очистки при анимации
        background = self.screen.subsurface(base_thumb_rect).copy()

        # цикл анимации появления
        for i in range(fps + 1):
            # чистим фон
            self.screen.blit(background, base_thumb_rect)
            # создаем Rect малого, пропорционально шагу, размера
            tmp_rect = pygame.Rect((0, 0), (step * i, step * i))
            tmp_rect.center = screen_rect.center
            thumb_rect = base_thumb_rect.fit(tmp_rect)
            # рисуем ее на экране
            self.screen.blit(pygame.transform.scale(base_thumb, (thumb_rect.w, thumb_rect.h)), thumb_rect)
            # обновляем экран
            pygame.display.update(tmp_rect)
            # тикаем ;)
            self.clock.tick(50)

        # подождем пока не нажмут мышь
        runing = True
        while runing:
            # опрос очереди событий
            for event in pygame.event.get():
                # если нажата мышь - устанавливаем флаг поимки равный букве, которую ловим
                if event.type == MOUSEBUTTONDOWN or event.type == JOYBUTTONDOWN or event.type == KEYDOWN:
                    runing = False
            # тикаем ;)
            self.clock.tick(50)

        ## цикл анимации удаления
        #x_size, y_size = (base_thumb_rect.w, base_thumb_rect.h)
        ## чистим фон
        #self.screen.blit(background, base_thumb_rect)
        ## рисуем картинку
        #self.screen.blit(base_thumb, base_thumb_rect)

        #for i in xrange(fps-1):
        #    # чистим фон
        #    self.screen.blit(background, base_thumb_rect)
        #    # уменьшаем картинку
        #    x_size -= step
        #    y_size -= step
        #    tmp_rect = pygame.Rect((0, 0), (x_size, y_size))
        #    tmp_rect.center = screen_rect.center
        #    # рисуем картинку
        #    self.screen.blit(pygame.transform.scale(base_thumb, (tmp_rect.w, tmp_rect.h)), tmp_rect)
        #    # обновляем экран
        #    pygame.display.update(base_thumb_rect)
        #    # тикаем ;)
        #    self.clock.tick(50)

    def catch_fail(self, fish_index):
        self.games_sounds.play_failchar(self.fishes[fish_index].get_char())

    def check_events(self):
            # опрос очереди событий
            for event in pygame.event.get():
                # выход, если событие выхода
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    sys.exit(0)

                # переключение в режим/из режима "полный экран"
                if event.type == KEYDOWN and event.key == K_f:
                    pygame.display.toggle_fullscreen()

                # если мышь двинулась
                if event.type == MOUSEMOTION:
                    # получаем позицию мыши
                    self.x, self.y = pygame.mouse.get_pos()

                # если джойстик двинулся
                if event.type == JOYAXISMOTION:
                    axis_val = event.value
                    if event.axis == 0:
                        self.x = event.value * self.SCREEN_RECT.w / 2.0 + self.SCREEN_RECT.h / 2.0
                        self.x = int(self.x)
                    elif event.axis == 1:
                        self.y = event.value * self.SCREEN_RECT.w / 2.0 + self.SCREEN_RECT.h / 2.0
                        self.y = int(self.y)

                # если нажата мышь, или клавиша на джойстике - устанавливаем флаг поимки равный букве, которую ловим
                if event.type == MOUSEBUTTONDOWN or event.type == JOYBUTTONDOWN:
                    self.catch = self.big_char

if __name__ == "__main__":
    try:
        os.chdir(os.path.sep.join(sys.argv[0].split(os.path.sep)[:-1]))
    except:
        pass
    g = Game()
    g.run()
