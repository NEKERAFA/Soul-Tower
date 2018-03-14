# -*- coding: utf-8 -*-

import pygame
from src.sprites.Character import *
from src.sprites.characters.NPC import *
from src.ResourceManager import *

class Enemy(NPC):
    def __init__(self, spriteName):
        NPC.__init__(self, spriteName)

    def move_ai(self, player):
        Character.move(self, E)
