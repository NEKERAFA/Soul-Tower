# -*- coding: utf-8 -*-

import pygame, math, sys
from src.sprites.behaviours.BehaviourState import *
from src.sprites.Character import *
from src.sprites.EnemyRange import *
from src.sprites.behaviours.PatrollState import PatrollState

# ------------------------------------------------------------------------------
# Clase FollowPlayerState

class FollowPlayerState(BehaviourState):
    def __init__(self, center, radius, vision):
        # Llamamos al constructor de la superclase
        BehaviourState.__init__(self)
        # Creo el rango de vision
        self.range = EnemyRange(radius, vision, 270)
        self.range.rect.center = center
        # Distancia con el jugador
        self.playerDist = 0

    def move_ai(self, enemy, player):
        # Obtenemos las posiciones del enemigo y el jugador
        (enemyX, enemyY) = enemy.rect.center
        (playerX, playerY) = player.rect.center
        # Actualizamos la distancia al jugador
        self.playerDist = math.hypot(playerX-enemyX, playerY-enemyY)
        # Obtenemos el ángulo entre el enemigo y el jugador
        playerAngle = int(math.degrees(math.atan2(enemyY-playerY, playerX-enemyY)))
        # Corrección cuando el ángulo es entre 180-360
        if playerAngle < 0:
            playerAngle = 360 + playerAngle
        # Calculamos hacia donde tiene que moverse el personaje
        (move, lookAt) = get_move(playerAngle)

        # Se actualiza el movimiento del personaje
        Character.move(enemy, move)

        # Se rota el rango de visión
        self.range.look_at(lookAt)

    def update(self, enemy, time, mapRect, mapMask):
        # Comprobamos que el enemigo no se ha salido del campo de visión o no
        # hay ningún obstáculo
        if (self.playerDist > self.range.radius):
            print "No veo al jugador"
            move = enemy.movement
            # Creamos el estado de seguir
            enemy.state = PatrollState(enemy.rect.center, self.range.radius, self.range.angle)
            # Establezcemos la dirección a donde mira
            enemy.state.range.look_at(self.range.lookAt)
            enemy.state.move = move
            # Ejecutamos el nuevo estado
            enemy.state.update(enemy, time, mapRect, mapMask)

        # Llamamos al update de characters
        Character.update(enemy, time, mapRect, mapMask)

        # Actualizamos la posición del campo de visión
        (enemyX, enemyY) = enemy.rect.center
        (rangeX, rangeY) = self.range.rect.center
        self.range.increment_position((enemyX-rangeX, enemyY-rangeY))

# Esta función discretiza un ángulo de dirección aleatorio de visión y devuelve
# un movimiento en ese ángulo y el ángulo que caracteriza
def get_move(angle):
    # Movimiento al este
    if angle < 22.5 or angle >= 337.5:
        return E, 0
    # Movimiento al noreste
    if angle >= 22.5 and angle < 67.5:
        return NE, 45
    # Movimiento al norte
    if angle >= 67.5 and angle < 112.5:
        return N, 90
    # Movimiento al noroeste
    if angle >= 112.5 and angle < 157.5:
        return NW, 135
    # Movimiento al oeste
    if angle >= 157.5 and angle < 202.5:
        return W, 180
    # Movimiento al suroeste
    if angle >= 202.5 and angle < 247.5:
        return SW, 225
    # Movimiento al sur
    if angle >= 247.5 and angle < 292.5:
        return S, 270
    # Movimiento al sureste
    if angle >= 292.5 and angle < 337.5:
        return SE, 315
