# -*- coding: utf-8 -*-

import pygame
from src.sprites.Character import *
from src.sprites.characters.NPC import *
from src.ResourceManager import *

class Enemy(NPC):
    def __init__(self, spriteName, drop):
        NPC.__init__(self, spriteName)
        self.drop = drop

    def move_ai(self, player):
        #Character.move(self, E)
        return
