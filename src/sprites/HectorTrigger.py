# -*- coding: utf-8 -*-

import pygame, os
from src.sprites.ConditionalTrigger import *

class HectorTrigger(ConditionalTrigger):
    def activate(self, player):
        if player.killedFriend:
            self.dialogueFile = self.dialogueList[0]
        else:
            self.dialogueFile = self.dialogueList[1]
