# -*- coding: utf-8 -*-

import random
from src.sprites.characters.behaviours.RavenBehaviourState import *
from src.sprites.Character import *
from src.sprites.MySprite import *
from src.sprites.EnemyRange import *

# ------------------------------------------------------------------------------
# Clase RavenStillState

class RavenStillState(RavenBehaviourState):
    def __init__(self):
        RavenBehaviourState.__init__(self)
        print "Raven: Still"

    def move_ai(self, enemy, player):
        pass

    def update(self, enemy, time, mapRect, mapMask):
        # Se actualiza la animación del personaje
        Character.update_animation(enemy, time)
        MySprite.update(enemy, time)

    def receive_damage(self, enemy, attack, damage, force):
        pass
