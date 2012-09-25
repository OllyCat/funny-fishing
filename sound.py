#!/usr/bin/env python
# coding: utf-8

# Created 2012-09-25

import os, sys, re
import pygame
from pygame.locals import *

class Sound:
    def __init__(self):
        self.voice = pygame.mixer.Channel(0)
        self.music = pygame.mixer.Channel(1)

        self.sounds = {}
        data_dir = os.listdir("sound")
        for i in data_dir:
            sound = pygame.mixer.Sound(os.path.join("sound", i))
            if not sound:
                print("Error! Sound file %s not found!" % i)
                os.exit(255)
            key = i.decode("utf-8")
            self.sounds[key] = sound

    def play_startchar(self, char):
        self.voice.play(self.sounds["start_char.ogg"])
        self.voice.set_volume(1.0)
        self.voice.queue(self.sounds[char + ".ogg"])

    def play_music(self):
        self.music.play(self.sounds["music.ogg"], loops = -1)
        self.music.set_volume(0.3)

    def play_failchar(self, char):
        self.voice.play(self.sounds["fail_char.ogg"])
        self.voice.set_volume(1.0)
        self.voice.queue(self.sounds[char + ".ogg"])

    def play_success(self):
        self.voice.play(self.sounds["success.ogg"])
        self.voice.set_volume(0.3)
