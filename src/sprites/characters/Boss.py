# -*- coding: utf-8 -*-

import pygame, random
from src.sprites.Character import *
from src.sprites.characters.Enemy import *
from src.sprites.Drop import *
from src.sprites.characters.behaviours.raven.RavenFlyAroundStageState import *
from src.sprites.characters.behaviours.death.DeathMainState import *
from src.sprites.characters.behaviours.master.MasterMainState import *

class Boss(Enemy):
    def __init__(self, name, drops, closeDoor, dialogueFile):
        self.behaviour = {"type": name}
        Enemy.__init__(self, name, drops[0])
        if len(drops) > 1:
            self.drops = drops[1:]
        else:
            self.drops = []
        self.closeDoor = closeDoor
        self.dialogueFile = dialogueFile
        if (name=="raven"):
            self.initialState = RavenFlyAroundStageState()
        elif (name=="death"):
            self.initialState = DeathMainState()
        elif (name=="master"):
            self.initialState = MasterMainState()
        else:
            raise NotImplementedError('Error: initial boss state not implemented')

    def set_drop(self, dropGroup):
        Enemy.set_drop(self, dropGroup)
        for drop in self.drops:
            offsetX = random.randint(-self.rect.width/2, self.rect.width/2)
            offsetY = random.randint(-self.rect.height, 0)
            x, y = self.rect.midbottom
            drop.change_position((x+offsetX, y+offsetY))
            dropGroup.add(drop)
