# -*- coding: utf-8 -*-

import pygame
from Character import *

class NPC(Character):
    def __init__(self, imageFile, spriteSheet, playerSpeed):
        Character.__init__(self, imageFile, spriteSheet, playerSpeed)

    def move_npc(self, player):
        #nada
        return
