# -*- coding: utf-8 -*-

import pygame, os
from src.sprites.MySprite import *

class Trigger(MySprite):

    def __init__(self, rect, dialogueFile):
        MySprite.__init__(self)
        self.rect = rect
        self.image = pygame.Surface((0,0)) # Le asignamos una imagen vacía
        self.dialogueFile = dialogueFile
    # No necesita actualizar nada
    def update(self, time):
        pass
