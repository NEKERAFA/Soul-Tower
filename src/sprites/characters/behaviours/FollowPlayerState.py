# -*- coding: utf-8 -*-

import pygame, math, sys
from src.sprites.characters.behaviours.BehaviourState import *
from src.sprites.Character import *
from src.sprites.EnemyRange import *
from src.sprites.characters.behaviours.PatrollState import PatrollState

# ------------------------------------------------------------------------------
# Clase FollowPlayerState

class FollowPlayerState(BehaviourState):
    def __init__(self, radius, angle, move):
        # Llamamos al constructor de la superclase
        BehaviourState.__init__(self)

        # Radio y angulo de apertura del campo de vision
        self.radius = radius
        self.angle = angle

        # Inicializo los valores de la distancia del jugador
        self.playerDistance = 0
        self.playerAngle = 0

    def move_ai(self, enemy, player):
        # Obtenemos las posiciones del enemigo y el jugador
        (enemyX, enemyY) = enemy.rect.center
        (playerX, playerY) = player.rect.center

        # Actualizamos la distancia al jugador
        self.playerDistance = math.hypot(playerX-enemyX, playerY-enemyY)

        # Obtenemos el ángulo entre el enemigo y el jugador
        self.playerAngle = int(math.degrees(math.atan2(enemyY-playerY, playerX-enemyX)))

        # Corrección cuando el ángulo es entre 180-360
        if self.playerAngle < 0:
            self.playerAngle = 360 + self.playerAngle

        # Calculamos hacia donde tiene que moverse el personaje
        lookAt, move = EnemyRange.discretice_angle(self.playerAngle)

        # Se actualiza el movimiento del personaje
        Character.move(enemy, move)

    def update(self, enemy, time, mapRect, mapMask):
        # Creo una imagen con una linea para saber si colisiona con el
        size = (self.radius*2, self.radius*2)
        line = pygame.Surface(size)
        center = (self.radius, self.radius)
        angle = math.radians(self.playerAngle+90)
        endX = self.radius*math.cos(angle)+self.radius
        endY = self.radius*math.sin(angle)+self.radius
        pygame.draw.line(line, (255, 255, 255), center, (endX, endY), 1)
        line.set_colorkey((0, 0, 0))

        # Creo la máscara para comprobar colisión con el mapa
        raytestMask = pygame.mask.from_surface(line)

        # Obtengo el offset
        x = enemy.rect.centerx-self.radius
        y = enemy.rect.centery-self.radius

        # Colisión con el mapa
        stageCollision = raytestMask.overlap(mapMask, (-x, -y))

        # Distancia al mapa infinita
        stageDistance = sys.maxint

        # Obtengo la distancia real si hay colisión
        if stageCollision is not None:
            stageCollision = (stageCollision[0]-self.radius, stageCollision[1]-self.radius)
            stageDistance = math.hypot(stageCollision[0], stageCollision[1])

        # Comprobamos que el jugador siga en rango o no haya una pared de por
        # medio
        if self.playerDistance > self.radius or self.playerDistance > stageDistance:
            # Creamos el estado de seguir
            enemy.state = PatrollState(enemy.rect.center, self.radius, self.angle, enemy.movement)

            # Ejecutamos el nuevo estado
            enemy.state.update(enemy, time, mapRect, mapMask)
            return

        # Llamamos al update de characters
        Character.update(enemy, time, mapRect, mapMask)
