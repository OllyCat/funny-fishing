#!/usr/bin/env python
# coding: utf-8

# Created 2012-09-18

"""
Основной скрипт. Содержит инициализации окна, классов и основную петлю с
обработкой событий.
"""

import pygame, sys, random, math, os
from pygame.locals import *
import sea, fish, hook

def run():
	# буква за которой охотимся
    big_char = u"А"
	# массив рыб
    fishes = []
	# список файлов рыб
    fish_pics = (
        "fish01.png",
        "fish02.png",
        "fish03.png",
    )

	# инициализация pygame
    pygame.init()
	# устанавливаем заголовок
    pygame.display.set_caption("Веселая рыбалка")
	# создаем окно
    screen = pygame.display.set_mode((1024, 768), HWSURFACE|DOUBLEBUF)
	# создаем море
    Sea = sea.Sea(screen)
	# создаем крючок и леску
    FishHook = hook.FishHook(screen)
	# таймер
    clock = pygame.time.Clock()

	# заполняем массив рыбами передавая путь до файлов
    for i in fish_pics:
        fishes.append(fish.Fish(screen, os.path.join("data",i)))

	# основной цикл
    while True:
	    # получаем позицию мыши
        x, y = pygame.mouse.get_pos()
	    # устанавливаем флаг поимки в False
        catch = False

	    # опрос очереди событий
        for event in pygame.event.get():
	        # выход, если событие выхода
            if event.type == QUIT:
                sys.exit(0)
	        # если нажата мышь - устанавливаем флаг поимки равный букве, которую ловим
            if event.type == MOUSEBUTTONDOWN:
                catch = big_char

	    # прорисовываем море
        Sea.update()

	    # в цикле обновляем всех рыб
        for j in fishes:
	        # рыбе передаем позицию курсора и флаг поимки, получаем False, если не поймана, или True, если поймана
            ret = j.update(x, y, catch)
	        # если поймана сбрасываем флаг поимки в False и сообщаем о пойманной рыбе.
            if ret:
                catch = False
                print "Поймал"

	    # обновляем крючок и леску
        FishHook.update(x, y)

	    # обновляем дисплей
        pygame.display.update()
	    # отсчитываем тики для задержки
        clock.tick(50)
    return

if __name__ == "__main__":
    run()
