# -*- coding: utf-8 -*-

import pygame, sys, os
from NPC import *

ENEMY_SPEED = 0.15

class Enemy(NPC):
    def __init__(self):
        NPC.__init__(self, 'characters/mage.png', 'mage.json', ENEMY_SPEED)

    def move_npc(self, player):
        #nada
        return