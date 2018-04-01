# -*- coding: utf-8 -*-

import pygame, os
from src.sprites.ConditionalTrigger import *

class PreEndingTrigger(ConditionalTrigger):
    def activate(self, player):
        if player.choseAnythingNotShared:
            if player.choiceAdder > 0:
                self.dialogueFile = self.dialogueList[0]
            elif player.choiceAdder < 0:
                self.dialogueFile = self.dialogueList[1]
            else:
                self.dialogueFile = self.dialogueList[randint(0, 1)]
        else:
            self.dialogueFile = self.dialogueList[2]
