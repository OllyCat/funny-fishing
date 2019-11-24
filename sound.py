#!/usr/bin/env python
# coding: utf-8

# Created 2012-09-25

import os
import sys
import re

import pygame
from pygame.locals import *


class Sound:
    def __init__(self):
        self.voice = pygame.mixer.Channel(0)
        self.music = pygame.mixer.music

        self.sounds = {}

        data_dir = os.listdir("sound")
        for i in data_dir:
            sound = pygame.mixer.Sound(os.path.join("sound", i))
            if not sound:
                print("Error! Sound file %s not found!" % i)
                os.exit(255)
            key = i
            self.sounds[key] = sound

        self.musics = []

        music_dir = os.listdir("music")
        for i in music_dir:
            m = os.path.join("music", i)
            if m:
                self.musics.append(m)

        self.music_index = 0

    def play_startchar(self, char):
        self.voice.play(self.sounds["start_char.ogg"])
        self.voice.set_volume(1.0)
        try:
            self.voice.queue(self.sounds[char + ".ogg"])
        except:
            print("ERROR: %s.ogg file not found " % char + ".ogg")
        self.music.set_volume(0.3)

    def play_music(self):
        # если музыка не найдена - просто вернуться
        if len(self.musics) == 0:
            return

        # если музыка играет - выходим, иначе начинаем смену трека
        if self.music.get_busy():
            return

        # установить миксер
        self.music.set_volume(0.3)
        # взять очередную песню
        m = self.musics[self.music_index]
        # загрузить
        self.music.load(m)
        # проиграть
        self.music.play()
        # изменить индекс
        self.music_index += 1
        # если это была последняя - начать плейлист сначала
        if self.music_index >= len(self.musics):
            self.music_index = 0

    def play_failchar(self, char):
        #self.voice.play(self.sounds["fail_char.ogg"])
        self.voice.set_volume(1.0)
        try:
            self.voice.queue(self.sounds[char + ".ogg"])
        except:
            print("ERROR: %s.ogg file not found " % char + ".ogg")
        self.music.set_volume(0.3)

    def play_success(self, char):
        self.voice.set_volume(1.0)
        #self.voice.play(self.sounds["success.ogg"])
        try:
            self.voice.play(self.sounds[char + ".ogg"])
        except:
            print("ERROR: %s.ogg file not found " % char + ".ogg")
