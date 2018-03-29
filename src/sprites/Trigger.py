# -*- coding: utf-8 -*-

import pygame, os
from src.sprites.MyStaticSprite import *

class Trigger(MyStaticSprite):
    def __init__(self, rect, dialogueFile, door):
        MyStaticSprite.__init__(self)
        self.rect = rect
        self.image = pygame.Surface((0,0)) # Le asignamos una imagen vacía
        self.dialogueFile = dialogueFile
        self.door = door

    def open_door(self, stage):
        if self.door is not None:
            self.door.open(stage)
