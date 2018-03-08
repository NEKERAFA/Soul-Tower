# -*- coding: utf-8 -*-

import pygame, sys, os
from pygame.locals import *
from Character import *

class NPC(Character):
    def __init__(self, imageFile, spriteSheet, playerSpeed):
        Character.__init__(self, imageFile, spriteSheet, playerSpeed)

    def move_npc(self, player):
        #nada
        return