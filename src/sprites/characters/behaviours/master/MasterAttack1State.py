# -*- coding: utf-8 -*-

import random
from src.sprites.characters.behaviours.MasterBehaviourState import *
from src.sprites.characters.behaviours.master.MasterMainState import *
from src.sprites.Character import *
from src.sprites.MySprite import *
from src.sprites.EnemyRange import *

# ------------------------------------------------------------------------------
# Clase MasterCastState

class MasterAttack1State(MasterBehaviourState):
    def __init__(self, previousState):
        MasterBehaviourState.__init__(self)
        self.previousState = previousState
        self.player = previousState.player
        # self.delayTime = random.randint(3, 4)*1000
        # self.elapseTime = 0

    def move_ai(self, enemy, player):
        pass

    def update(self, enemy, time, mapRect, mapMask):
        # Se actualiza la animación del personaje
        Character.update_animation(enemy, time)
        MySprite.update(enemy, time)
        # print(enemy.animationFinish)

        # # Si se acaba la primera parte de la animación
        # # se comienza en loop la siguiente
        # if (enemy.animationNum==7 and enemy.animationFinish):
        #     enemy.set_initial_frame(8)
        #     enemy.animationFinish = False
        #     enemy.animationLoop = True

        # # En esta animación se puede atacar
        # if enemy.animationNum == 8:
        #     # Actualizamos el tiempo interno
        #     self.elapseTime += time

        if (enemy.animationFrame==3):
            y = enemy.rect.bottom
            x = enemy.rect.left + enemy.rect.width/2
            # Indicamos que se puede atacar
            enemy.attack.start_attack((x,y), self.player.rect.center)

            if (enemy.animationFinish == True):
                # self.elapseTime += time
                # Si se pasan los segundos, cambio de estado
                enemy.animationFinish = False
                enemy.animationLoop = True
                enemy.attack.end_attack()
                enemy.change_behaviour(self.previousState)
