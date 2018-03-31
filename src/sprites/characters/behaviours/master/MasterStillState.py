# -*- coding: utf-8 -*-

import random
from src.sprites.characters.behaviours.MasterBehaviourState import *
# from src.sprites.characters.behaviours.death.MasterFollowPlayerState import *
from src.sprites.Character import *
from src.sprites.MySprite import *
from src.sprites.EnemyRange import *

# ------------------------------------------------------------------------------
# Clase MasterStillState

class MasterStillState(MasterBehaviourState):
    def __init__(self):
        MasterBehaviourState.__init__(self)

    def move_ai(self, enemy, player):
        pass

    def update(self, enemy, time, mapRect, mapMask):
        # Se actualiza la animación del personaje
        Character.update_animation(enemy, time)
        MySprite.update(enemy, time)

    def receive_damage(self, enemy, attack, damage, force):
        pass