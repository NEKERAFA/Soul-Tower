# -*- coding: utf-8 -*-

import pygame
from Character import *

class NPC(Character):
    def __init__(self, spriteName, speed):
        Character.__init__(self, imageFile, spriteSheet, speed)

    def move_ai(self, player):
        raise NotImplementedError('Error: Abstract class')
