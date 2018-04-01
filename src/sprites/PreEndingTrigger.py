# -*- coding: utf-8 -*-

import pygame, os, random
from src.sprites.ConditionalTrigger import *

class PreEndingTrigger(ConditionalTrigger):
    def activate(self, player):
        if player.choseAnythingNotShared:
            if player.choiceAdder > 0:
                self.dialogueFile = self.dialogueList[0]
                player.canChange = False
                if player.currentCharacter != 'sorcerer':
                    player.change_character()
            elif player.choiceAdder < 0:
                player.canChange = False
                self.dialogueFile = self.dialogueList[1]
                if player.currentCharacter != 'warrior':
                    player.change_character()
            else:
                player.choiceAdder = random.choice([-1,1])
                self.activate(player)
        else:
            self.dialogueFile = self.dialogueList[2]
