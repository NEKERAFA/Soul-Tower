# -*- coding: utf-8 -*-

import random
from src.sprites.characters.behaviours.DeathBehaviourState import *
# from src.sprites.characters.behaviours.death.DeathFollowPlayerState import *
from src.sprites.characters.behaviours.death.DeathMainState import *
from src.sprites.Character import *
from src.sprites.MySprite import *
from src.sprites.EnemyRange import *

# ------------------------------------------------------------------------------
# Clase DeathSlashState

class DeathSlashState(DeathBehaviourState):
    def __init__(self, previousState):
        DeathBehaviourState.__init__(self)
        self.previousState = previousState
        self.player = self.previousState.player

    def move_ai(self, enemy, player):
        pass

    def update(self, enemy, time, mapRect, mapMask):

        Character.update_animation(enemy, time)
        MySprite.update(enemy, time)
        if enemy.animationFrame > 0:
            # Obtenemos las posiciones del enemigo y el jugador
            (enemyX, enemyY) = enemy.rect.center
            (playerX, playerY) = self.player.rect.center

            # Obtenemos el ángulo entre el enemigo y el jugador
            angle = int(math.degrees(math.atan2(enemyY-playerY, playerX-enemyX)))

            # Corrección cuando el ángulo es entre 180-360
            if angle < 0:
                angle = 360 + angle
            enemy.attack.start_attack(enemy.rect.topleft, angle)

        if (enemy.animationFinish):
            enemy.animationLoop = True
            enemy.animationFinish = False
            enemy.attack = None
            enemy.change_behaviour(DeathMainState())
