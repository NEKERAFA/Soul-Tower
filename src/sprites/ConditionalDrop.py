# -*- coding: utf-8 -*-

from src.sprites.Drop import *

class ConditionalDrop(Drop):
    def __init__(self, spriteName, dialogueList):
        Drop.__init__(self, spriteName, 0)
        self.dialogueList = dialogueList

    def collect(self, stage):
        raise NotImplementedError("Must implement collect")
