# -*- coding: utf-8 -*-

import pygame, math, sys
from src.sprites.characters.behaviours.BehaviourState import *
from src.sprites.characters.behaviours.FollowPlayerState import *
from src.sprites.Character import *

# ------------------------------------------------------------------------------
# Clase StillState

class StillState(BehaviourState):
    def __init__(self, radius):
        # Llamamos al constructor de la superclase
        BehaviourState.__init__(self)
        self.distance = sys.maxint
        self.angle = 0
        self.radius = radius

    def move_ai(self, enemy, player):
        # Obtenemos las posiciones del enemigo y el jugador
        (enemyX, enemyY) = enemy.rect.center
        (playerX, playerY) = player.rect.center

        # Actualizamos la distancia al jugador
        self.distance = math.hypot(playerX-enemyX, playerY-enemyY)

        # Obtenemos el ángulo entre el enemigo y el jugador
        self.angle = int(math.degrees(math.atan2(enemyY-playerY, playerX-enemyX)))

        # Se actualiza el movimiento del personaje
        if enemy.movement != STILL:
            Character.move(enemy, STILL)

    def update(self, enemy, time, mapRect, mapMask):
        # Creo una imagen con una linea para saber si colisiona con el fondo
        size = (self.radius*2, self.radius*2)
        line = pygame.Surface(size)
        center = (self.radius, self.radius)
        angle = math.radians(self.angle+90)
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

        # Comprobamos que el jugador esté en el rango y no haya una pared antes
        if self.distance < self.radius and self.distance < stageDistance:
            # Volvemos al estado anterior
            enemy.change_behaviour(FollowPlayerState(self.radius, self))
            return

        # Llamamos al update de characters
        Character.update(enemy, time, mapRect, mapMask)
