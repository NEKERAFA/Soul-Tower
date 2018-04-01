# -*- coding: utf-8 -*-

import pygame, os, random
from src.sprites.ConditionalTrigger import *

class FinalBossTrigger(ConditionalTrigger):
    def activate(self, player):
        if player.choseAnythingNotShared:
            if player.choiceAdder > 0:
                self.dialogueFile = self.dialogueList[0]
            elif player.choiceAdder < 0:
                self.dialogueFile = self.dialogueList[1]
            else:
                print "This should not happen"
        else:
            self.dialogueFile = self.dialogueList[2]
