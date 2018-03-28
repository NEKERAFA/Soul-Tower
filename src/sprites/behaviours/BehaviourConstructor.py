# -*- coding: utf-8 -*-

import pygame
from src.sprites.behaviours.PatrollState import *
from src.sprites.behaviours.WanderingState import *

class BehaviourConstructor(object):
    @classmethod
    def get_behaviour(cls, behaviourName, enemy):
        if behaviourName == 'wandering':
            return WanderingState()
        elif behaviourName == 'patrolling':
            return PatrollState(enemy.rect.center, enemy.behaviour["radius"], math.radians(enemy.behaviour["angle"]), STILL)
        else:
            raise SystemExit, 'behaviour not permited'
