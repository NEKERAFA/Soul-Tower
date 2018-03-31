# -*- coding: utf-8 -*-

import random
from src.sprites.characters.behaviours.MasterBehaviourState import *
from src.sprites.Character import *
from src.sprites.MySprite import *
from src.sprites.EnemyRange import *

# ------------------------------------------------------------------------------
# Clase MasterMainState

class MasterMainState(MasterBehaviourState):
    def __init__(self):
        MasterBehaviourState.__init__(self)
        self.delayTime = random.randint(1, 2)*1000
        self.elapseTime = 0

    def move_ai(self, enemy, player):
        pass

    def update(self, enemy, time, mapRect, mapMask):
        # Actualizamos el tiempo interno
        self.elapseTime += time
        # Se actualiza la animación del personaje
        Character.move(enemy, STILL)
        Character.update_movement(enemy, time)
        # Character.update_animation(enemy, time)
        MySprite.update(enemy, time)

        # Si se pasan los segundos volando, cambio de estado
        if self.elapseTime > self.delayTime:
            self.delayTime = random.randint(1, 2)*1000
            self.elapseTime = 0
            enemy.change_behaviour(MasterFollowPlayerState(self))

from src.sprites.characters.behaviours.master.MasterFollowPlayerState import *