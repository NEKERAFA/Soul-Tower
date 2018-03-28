# -*- coding: utf-8 -*-

import pygame, random
from src.sprites.Character import *
from src.sprites.characters.Enemy import *
from src.sprites.Drop import *

class Boss(Enemy):
    def __init__(self, name, drops):
        if name == 'raven':
            self.behaviour = {"type": "ravenBehaviour"}
        Enemy.__init__(self, name, drops[0])
        self.drops = drops[1:]

    def set_drop(self, dropGroup):
        Enemy.set_drop(self, dropGroup)
        for drop in self.drops:
            offsetX = random.randint(-self.rect.width/2, self.rect.width/2)
            offsetY = random.randint(-self.rect.height, 0)
            x, y = self.rect.midbottom
            drop.change_position((x+offsetX, y+offsetY))
            dropGroup.add(drop)
