# -*- coding: utf-8 -*-

import pygame, os, sys
from src.sprites.Trigger import *

class ConditionalTrigger(Trigger):
    def __init__(self, rect, dialogueList):
        Trigger.__init__(self, rect, None, None)
        self.dialogueList = dialogueList

    def activate(self, player):
        raise NotImplementedError("Must implement activate")
