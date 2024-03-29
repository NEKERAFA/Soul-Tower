# -*- coding: utf-8 -*-

import random
from src.sprites.characters.behaviours.DeathBehaviourState import *
# from src.sprites.characters.behaviours.death.DeathFollowPlayerState import *
from src.sprites.characters.behaviours.death.DeathMainState import *
from src.sprites.Character import *
from src.sprites.MySprite import *
from src.sprites.EnemyRange import *

# ------------------------------------------------------------------------------
# Clase DeathCastState

class DeathCastState(DeathBehaviourState):
    def __init__(self, previousState):
        DeathBehaviourState.__init__(self)
        self.player = previousState.player
        self.delayTime = random.randint(3, 4)*1000
        self.elapseTime = 0

    def move_ai(self, enemy, player):
        pass

    def update(self, enemy, time, mapRect, mapMask):
        # Se actualiza la animación del personaje
        Character.update_animation(enemy, time)
        MySprite.update(enemy, time)

        # Si se acaba la primera parte de la animación
        # se comienza en loop la siguiente
        if (enemy.animationNum==7 and enemy.animationFinish):
            enemy.set_initial_frame(8)
            enemy.animationFinish = False
            enemy.animationLoop = True

        # En esta animación se puede atacar
        if enemy.animationNum == 8:
            # Actualizamos el tiempo interno
            self.elapseTime += time

            # Indicamos que se puede atacar
            enemy.attack.start_attack(enemy.rect.topleft, self.player.rect.center)

            # Si se pasan los segundos, cambio de estado
            if self.elapseTime > self.delayTime:
                self.delayTime = random.randint(1, 3)*1000
                self.elapseTime = 0
                enemy.attack.end_attack()
                enemy.change_behaviour(DeathMainState())
