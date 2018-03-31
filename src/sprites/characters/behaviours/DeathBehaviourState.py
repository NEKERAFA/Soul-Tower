# -*- coding: utf-8 -*-

from src.sprites.characters.behaviours.BehaviourState import *

# ------------------------------------------------------------------------------
# Clase DeathBehaviourState

class DeathBehaviourState(BehaviourState):

    def receive_damage(self, enemy, attack, damage, force):
        BehaviourState.receive_damage(self, enemy, attack, damage, 0)

