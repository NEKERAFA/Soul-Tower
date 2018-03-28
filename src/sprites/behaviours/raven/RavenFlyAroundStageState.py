# -*- coding: utf-8 -*-

import random
from src.sprites.behaviours.RavenBehaviourState import *

# ------------------------------------------------------------------------------
# Clase RavenFlyAroundStageState

class RavenFlyAroundStageState(RavenBehaviourState):
    def __init__(self):
        self.time = 0
        self.angle = random.int

    def move_ai(self, enemy, player):
        pass

    def update(self, enemy, time, mapRect, mapMask):
