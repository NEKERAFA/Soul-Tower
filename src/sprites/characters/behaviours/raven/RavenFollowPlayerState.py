# -*- coding: utf-8 -*-

import random
from src.sprites.characters.behaviours.RavenBehaviourState import *
from src.sprites.Character import *
from src.sprites.MySprite import *
from src.sprites.EnemyRange import *

# ------------------------------------------------------------------------------
# Clase RavenFollowPlayerState

class RavenFollowPlayerState(RavenBehaviourState):
    def __init__(self, previousState):
        RavenBehaviourState.__init__(self)
        # Estado previo
        self.previousState = previousState

    def move_ai(self, enemy, player):
        # Obtenemos las posiciones del enemigo y el jugador
        (enemyX, enemyY) = enemy.rect.center
        (playerX, playerY) = player.rect.center

        # Obtenemos el ángulo entre el enemigo y el jugador
        angle = int(math.degrees(math.atan2(enemyY-playerY, playerX-enemyX)))

        # Corrección cuando el ángulo es entre 180-360
        if angle < 0:
            angle = 360 + angle

        # Calculamos hacia donde tiene que moverse el personaje
        lookAt, move = EnemyRange.discretice_angle(angle)

        # Se actualiza el movimiento del personaje
        Character.move(enemy, move)

    def update(self, enemy, time, mapRect, mapMask):
        # Se actualiza el movimiento del personaje
        Character.update_movement(enemy, time)
        MySprite.update(enemy, time)

        # Comprobamos si se está colisionando con el enemigo para volver al
        # otro estado
        if pygame.sprite.collide_rect(player, enemy):
            enemy.change_behaviour(self.previousState)
            self.previousState.angle = int(angle+180)
            if self.previousState.angle > 360:
                self.previousState.angle -= 360
