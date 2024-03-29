# -*- coding: utf-8 -*-

import pygame
from src.sprites.Door import *
from src.sprites.Interactive import *

class UnlockedDoor(Door, Interactive):
    def __init__(self, position, imagePath, doorMask, stage, collision, key=None):
        Door.__init__(self, position, imagePath, doorMask, stage)
        Interactive.__init__(self, collision)
        self.key = key

    def activate(self, stage):
        if self.key is None or self.key in stage.player.inventory:
            self.open(stage)
