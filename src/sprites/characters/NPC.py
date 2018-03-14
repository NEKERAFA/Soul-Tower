# -*- coding: utf-8 -*-

import pygame
from src.sprites.Character import *

class NPC(Character):
    def __init__(self, spriteName):
        Character.__init__(self, spriteName)

    def move_ai(self, player):
        raise NotImplementedError('Error: Abstract class')
