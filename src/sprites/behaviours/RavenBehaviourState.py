# -*- coding: utf-8 -*-

from src.sprites.behaviours.BehaviourState import *

# ------------------------------------------------------------------------------
# Clase RavenBehaviourState

class RavenBehaviourState(BehaviourState):
    def move_ai(self, enemy, player):
        raise NotImplemented("Tiene que implementar el metodo move_ai.")

    def update(self, enemy, time, mapRect, mapMask):
        raise NotImplemented("Tiene que implementar el metodo update")
