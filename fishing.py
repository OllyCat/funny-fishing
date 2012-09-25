#!/usr/bin/env python
# coding: utf-8

# Created 2012-09-18

"""
Основной скрипт. Содержит инициализации окна, классов и основную петлю с
обработкой событий.
"""

import pygame, sys, random, math, os, re
from pygame.locals import *
import sea, fish, hook, ubar, sound

SCREEN_RECT = pygame.Rect((0, 0), (1024, 768))
BAR_RECT    = pygame.Rect((0, 0), (SCREEN_RECT.w, 60))
SEA_RECT    = pygame.Rect((0, BAR_RECT.h), (SCREEN_RECT.w, SCREEN_RECT.h - BAR_RECT.h))

def run():
	# массив рыб
    fishes = []
	# заполняем список файлов рыб
    data_dir = os.listdir("data")
    # выбираем только файлы рыб
    fish_pics = re.findall("fish\d\d.png", ''.join(data_dir))
    if len(fish_pics) == 0:
        print("Error! Fish pics not found!")
        sys.exit(255)

	# инициализация pygame
    pygame.init()
	# устанавливаем заголовок
    pygame.display.set_caption("Веселая рыбалка")
	# создаем окно
    screen = pygame.display.set_mode((SCREEN_RECT.w, SCREEN_RECT.h), HWSURFACE|DOUBLEBUF)

    # создаем верхний бар
    u_bar = ubar.UBar(screen, BAR_RECT)
    u_bar.draw()

    # загружаем звуки
    games_sounds = sound.Sound()
    # включаем музыку
    games_sounds.play_music()

	# буква за которой охотимся
    big_char = u_bar.get_curchar()
    # попросим поймать начальную букву
    games_sounds.play_startchar(big_char)

	# создаем море
    Sea = sea.Sea(screen, SEA_RECT)
	# создаем крючок и леску
    FishHook = hook.FishHook(screen, SEA_RECT)
    FishHook.update(pygame.mouse.get_pos())
	# таймер
    clock = pygame.time.Clock()
    # инициализируем джойстик, если есть
    if pygame.joystick.get_count() > 0:
        joy = pygame.joystick.Joystick(0)
        joy.init()

	# заполняем массив рыбами передавая путь до файлов
    for i in xrange(3):
        fishes.append(fish.Fish(screen, SEA_RECT, os.path.join("data", random.choice(fish_pics)), big_char))

    # получаем позицию мыши
    x, y = pygame.mouse.get_pos()

	# основной цикл
    while True:
	    # устанавливаем флаг поимки в False
        catch = False

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
                x, y = pygame.mouse.get_pos()

	        # если джойстик двинулся
            if event.type == JOYAXISMOTION:
                axis_val = event.value
                if event.axis == 0:
                    x = event.value * SCREEN_RECT.w/2.0 + SCREEN_RECT.h/2.0
                    x = int(x)
                elif event.axis == 1:
                    y = event.value * SCREEN_RECT.w/2.0 + SCREEN_RECT.h/2.0
                    y = int(y)

	        # если нажата мышь, или клавиша на джойстике - устанавливаем флаг поимки равный букве, которую ловим
            if event.type == MOUSEBUTTONDOWN or event.type == JOYBUTTONDOWN:
                catch = big_char

	    # прорисовываем море
        Sea.update()

	    # в цикле обновляем всех рыб
        for j in fishes.__reversed__():
	        # рыбе передаем позицию курсора и флаг поимки, получаем False, если не поймана, или True, если поймана
            ret = j.update(x, y)

	    # обновляем крючок и леску
        FishHook.update((x, y))

	    # обновляем дисплей
        pygame.display.update()

        # обнаруживаем пересечение объектов, если при этом стоит флаг поимки и
        # буква рыбы совпадает с искомой буквой, то рыба поймана, если не
        # совпадает - то не поймана и разворачивается
        fish_index = FishHook.rect.collidelist(map(lambda x: x.rect, fishes))
        if catch and fish_index >= 0:
            if fishes[fish_index].get_char() == catch:
                u_bar.update(catch)
                catch = False
                new_char = u_bar.get_curchar()
                fishes[fish_index].show_fish()
                cached_fish = fishes.pop(fish_index)
                games_sounds.play_success()
                catch_success(screen)
                fishes.append(fish.Fish(screen, SEA_RECT, os.path.join("data", random.choice(fish_pics)), big_char))
                if new_char <> big_char:
                    big_char = new_char
                    games_sounds.play_startchar(big_char)
            else:
                fishes[fish_index].set_reverse()
                games_sounds.play_failchar(fishes[fish_index].get_char())
                catch_fail()

	    # отсчитываем тики для задержки
        clock.tick(50)
    return

def catch_success(screen):
    clock = pygame.time.Clock()
    screen.set_clip()

    # количество шагов приближения картинки
    fps = 30
    # загружаем картинку
    base_thumb = pygame.image.load(os.path.join("data", "thumbs_up.png")).convert_alpha()
    # получаем размеры экрана, на котором рисуем и размер картинки
    screen_rect = screen.get_rect()
    base_thumb_rect = base_thumb.get_rect()
    base_thumb_rect.center = screen_rect.center
    # шаг увеличения картинки
    step = base_thumb_rect.h/fps
    # сохраним кусок экрана для очистки при анимации
    background = screen.subsurface(base_thumb_rect).copy()

    # цикл анимации появления
    for i in xrange(fps+1):
        # чистим фон
        screen.blit(background, base_thumb_rect)
        # создаем Rect малого, пропорционально шагу, размера
        tmp_rect = pygame.Rect((0, 0), (step * i, step * i))
        tmp_rect.center = screen_rect.center
        thumb_rect = base_thumb_rect.fit(tmp_rect)
        # рисуем ее на экране
        screen.blit(pygame.transform.scale(base_thumb, (thumb_rect.w, thumb_rect.h)), thumb_rect)
        # обновляем экран
        pygame.display.update(tmp_rect)
        # тикаем ;)
        clock.tick(50)

    # подождем пока не нажмут мышь
    runing = True
    while runing:
	    # опрос очереди событий
        for event in pygame.event.get():
	        # если нажата мышь - устанавливаем флаг поимки равный букве, которую ловим
            if event.type == MOUSEBUTTONDOWN or event.type == JOYBUTTONDOWN or event.type == KEYDOWN:
                runing = False
        # тикаем ;)
        clock.tick(50)

    ## цикл анимации удаления
    #x_size, y_size = (base_thumb_rect.w, base_thumb_rect.h)
    ## чистим фон
    #screen.blit(background, base_thumb_rect)
    ## рисуем картинку
    #screen.blit(base_thumb, base_thumb_rect)

    #for i in xrange(fps-1):
    #    # чистим фон
    #    screen.blit(background, base_thumb_rect)
    #    # уменьшаем картинку
    #    x_size -= step
    #    y_size -= step
    #    tmp_rect = pygame.Rect((0, 0), (x_size, y_size))
    #    tmp_rect.center = screen_rect.center
    #    # рисуем картинку
    #    screen.blit(pygame.transform.scale(base_thumb, (tmp_rect.w, tmp_rect.h)), tmp_rect)
    #    # обновляем экран
    #    pygame.display.update(base_thumb_rect)
    #    # тикаем ;)
    #    clock.tick(50)

def catch_fail():
    print "Мазила!"

if __name__ == "__main__":
    run()
