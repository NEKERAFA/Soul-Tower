# -*- coding: utf-8 -*-

import pygame
from NPC import *

ENEMY_SPEED = 0.15

class Enemy(NPC):
    def __init__(self, spriteName, speed = ENEMY_SPEED):
        NPC.__init__(self, spriteName, speed)

    def move_npc(self, player):
        return
