# -*- coding: utf-8 -*-

import pygame, os
from src.sprites.MySprite import *
# TODO cambiar superclase a MyStaticSprite
class Trigger(MySprite):

    def __init__(self, rect, dialogueFile):
        MySprite.__init__(self)
        self.rect = rect
        self.image = pygame.Surface((0,0)) # Le asignamos una imagen vacía
        self.dialogueFile = dialogueFile
