# -*- coding: utf-8 -*-

import pygame, math
from src.sprites.Character import *
from src.sprites.characters.NPC import *
from src.sprites.behaviours.WanderingState import *
from src.sprites.behaviours.PatrollState import *
from src.ResourceManager import *

class Enemy(NPC):
    def __init__(self, spriteName, drop):
        NPC.__init__(self, spriteName)
        self.drop = drop

        if self.behaviour is not None:
            if self.behaviour["type"] == "wandering":
                self.state = WanderingState()
            if self.behaviour["type"] == "patrolling":
                self.state = PatrollState(self.rect.center, self.behaviour["radius"], math.radians(self.behaviour["angle"]))

    def move_ai(self, player):
        self.state.move_ai(self, player)

    def update(self, time, mapRect, mapMask):
        self.state.update(self, time, mapRect, mapMask)
