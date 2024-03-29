# -*- coding: utf-8 -*-

import pygame, random
from src.sprites.Character import *
from src.sprites.characters.Enemy import *
from src.sprites.Drop import *
from src.sprites.characters.behaviours.raven.RavenFlyAroundStageState import *
from src.sprites.characters.behaviours.raven.RavenStillState import *
from src.sprites.characters.behaviours.death.DeathMainState import *
from src.sprites.characters.behaviours.master.MasterMainState import *
from src.sprites.characters.behaviours.master.MasterStillState import *

class Boss(Enemy):
    def __init__(self, name, drops, closeDoor, dialogueFile, deathAnimation=None):
        self.behaviour = {"type": name}
        Enemy.__init__(self, name, drops[0])
        # Iniciamos la animación del boss
        self.set_initial_frame(4)
        self.animationLoop = False
        if len(drops) > 1:
            self.drops = drops[1:]
        else:
            self.drops = []
        self.closeDoor = closeDoor
        self.dialogueFile = dialogueFile
        if (name=="raven"):
            self.initialState = RavenFlyAroundStageState()
            self.stillState = RavenStillState()
        elif (name=="death"):
            self.initialState = DeathMainState()
            self.stillState = DeathStillState()
        elif (name=="master"):
            self.initialState = MasterMainState()
            self.stillState = RavenStillState()
        else:
            raise NotImplementedError('Error: initial boss state not implemented')
        if deathAnimation is not None:
            self.hasDeathAnimation = True
            self.deathAnimation = deathAnimation
        else:
            self.hasDeathAnimation = False

    def set_drop(self, dropGroup):
        Enemy.set_drop(self, dropGroup)
        for drop in self.drops:
            offsetX = random.randint(-self.rect.width/2, self.rect.width/2)
            offsetY = random.randint(-self.rect.height, 0)
            x, y = self.rect.midbottom
            drop.change_position((x+offsetX, y+offsetY))
            dropGroup.add(drop)
