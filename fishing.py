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

SCREEN_X = 1024
SCREEN_Y = 768

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
    screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y), HWSURFACE|DOUBLEBUF)
	# создаем море
    Sea = sea.Sea(screen)
	# создаем крючок и леску
    FishHook = hook.FishHook(screen)
	# таймер
    clock = pygame.time.Clock()
    # инициализируем джойстик, если есть
    if pygame.joystick.get_count() > 0:
        joy = pygame.joystick.Joystick(0)
        joy.init()

	# заполняем массив рыбами передавая путь до файлов
    for i in fish_pics:
        fishes.append(fish.Fish(screen, os.path.join("data",i)))

    # получаем позицию мыши
    x, y = pygame.mouse.get_pos()

	# основной цикл
    while True:
	    # устанавливаем флаг поимки в False
        catch = False
        catched = False

	    # опрос очереди событий
        for event in pygame.event.get():
	        # выход, если событие выхода
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                sys.exit(0)

	        # если мышь двинулась
            if event.type == MOUSEMOTION:
                # получаем позицию мыши
                x, y = pygame.mouse.get_pos()

	        # если джойстик двинулся
            if event.type == JOYAXISMOTION:
                axis_val = event.value
                if event.axis == 0:
                    x = event.value * SCREEN_X/2.0 + SCREEN_X/2.0
                    x = int(x)
                elif event.axis == 1:
                    y = event.value * SCREEN_Y/2.0 + SCREEN_Y/2.0
                    y = int(y)

	        # если нажата мышь, или клавиша на джойстике - устанавливаем флаг поимки равный букве, которую ловим
            if event.type == MOUSEBUTTONDOWN or event.type == JOYBUTTONDOWN:
                catch = big_char

	    # прорисовываем море
        Sea.update()

	    # в цикле обновляем всех рыб
        for j in fishes:
	        # рыбе передаем позицию курсора и флаг поимки, получаем False, если не поймана, или True, если поймана
            ret = j.update(x, y, catch)
	        # если поймана ставим флаг
            if catch and ret:
                catched = j

        # если рыба поймана сбрасываем флаг поимки, отображаем пойманную рыбу с сбрасываем флаг пойманной рыбы
        if catch and catched:
            catch = False
            catched.show_fish()
            catched = False
            catch_success(screen)
        elif catch and not catched:
            catch_fail()

	    # обновляем крючок и леску
        FishHook.update(x, y)

	    # обновляем дисплей
        pygame.display.update()
	    # отсчитываем тики для задержки
        clock.tick(50)
    return

def catch_success(screen):
    clock = pygame.time.Clock()

    pygame.mouse.set_visible(True)

    # количество шагов приближения картинки
    fps = 30
    # загружаем картинку
    base_thumb = pygame.image.load(os.path.join("data", "thumbs_up.png")).convert_alpha()
    # получаем размеры экрана, на котором рисуем и размер картинки
    screen_size = screen.get_size()
    thumb_size = base_thumb.get_size()
    # шаг увеличения картинки
    step = (thumb_size[0]/fps, thumb_size[1]/fps)

    # цикл анимации
    for i in xrange(fps):
        # уменьшаем базовую картинку
        thumb = pygame.transform.scale(base_thumb, (step[0] * (i + 1), step[1] * (i + 1)))
        # получаем ее размер
        thumb_size = thumb.get_size()
        # рисуем ее на экране
        screen.blit(thumb, (screen_size[0]/2 - thumb_size[0]/2, screen_size[1]/2 - thumb_size[1]/2))
        # обновляем экран
        pygame.display.update()
        # тикаем ;)
        clock.tick(50)

    # подождем пока не нажмут мышь
    while True:
	    # опрос очереди событий
        for event in pygame.event.get():
	        # если нажата мышь - устанавливаем флаг поимки равный букве, которую ловим
            if event.type == MOUSEBUTTONDOWN or event.type == JOYBUTTONDOWN or event.type == KEYDOWN:
                return
        # тикаем ;)
        clock.tick(50)

def catch_fail():
    print "Мазила!"

if __name__ == "__main__":
    run()
