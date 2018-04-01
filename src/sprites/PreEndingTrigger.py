# -*- coding: utf-8 -*-

import pygame, os
from src.sprites.ConditionalTrigger import *

class PreEndingTrigger(ConditionalTrigger):
    def activate(self, player):
        if player.choseAnythingNotShared:
            if player.choiceAdder > 0:
                self.dialogueFile = self.dialogueList[0]
                if player.currentCharacter != 'sorcerer':
                    player.change_character()
                    player.canChange = False
            elif player.choiceAdder < 0:
                self.dialogueFile = self.dialogueList[1]
                if player.currentCharacter != 'warrior':
                    player.change_character()
                    player.canChange = False
            else:
                self.dialogueFile = self.dialogueList[randint(0, 1)]
                
        else:
            self.dialogueFile = self.dialogueList[2]
