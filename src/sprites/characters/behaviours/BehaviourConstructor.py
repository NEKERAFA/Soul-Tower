# -*- coding: utf-8 -*-

import pygame

from src.sprites.characters.behaviours.WanderingState import *
from src.sprites.characters.behaviours.PatrollState import *
from src.sprites.characters.behaviours.StillState import *
from src.sprites.characters.behaviours.raven.RavenStillState import *

class BehaviourConstructor(object):
    @classmethod
    def get_behaviour(cls, behaviourName, enemy):
        if behaviourName == 'wandering':
            return WanderingState()
        elif behaviourName == 'patrolling':
            return PatrollState(enemy.rect.center, enemy.behaviour["radius"], math.radians(enemy.behaviour["angle"]))
        elif behaviourName == 'waiting':
            return StillState(enemy.behaviour["radius"])
        elif behaviourName == 'raven':
            return RavenStillState()
        else:
            raise SystemExit, 'behaviour not permited'
