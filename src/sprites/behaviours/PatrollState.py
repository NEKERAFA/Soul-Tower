# -*- coding: utf-8 -*-

import pygame, random, math, sys
from src.sprites.behaviours.BehaviourState import *
from src.sprites.Character import *
from src.sprites.EnemyRange import *

# ------------------------------------------------------------------------------
# Clase PatrollState

# TODO Ajustar aquí
MAX_DELAY = 2000
MIN_DELAY = 500

MOVEMENTS = [N, NW, W, SW, S, SE, E, NE]

class PatrollState(BehaviourState):
    '''
        center: (int, int), Punto centrar sobre el que situar el rango de
        visión.
        radius: int, Radio de acción del rango.
        vision: float, Ángulo de vision del enemigo.
    '''
    def __init__(self, center, radius, vision):
        # Rango de patrulla
        self.patrollRange = EnemyRange(radius, vision, math.radians(270))
        # Lo centramos en el enemigo
        self.patrollRange.rect.center = enemy.rect.center
        # Empieza parado y con un tiempo random
        self.move = STILL
        self.delay = random.randint(MIN_DELAY, MAX_DELAY)
        # Inicializa los puntos de colisión
        self.playerCollision = None
        self.count = 0

    def move_ai(self, enemy, player):
        # Si se acaba el tiempo, cambia el movimiento
        if self.delay <= 0:
            # Si estaba pausado, se mueve
            if self.move == STILL:
                self.move = random.choice(MOVEMENTS)
            # Si se estaba moviendo, se pausa
            else:
                self.move = STILL
            # Tiempo aleatorioNone
            self.delay = random.randint(MIN_DELAY, MAX_DELAY)
            # Se mueve
            Character.move(enemy, self.move)
            # Hago que la máscara apunte a donde el personaje mira
            if self.move == E:
                self.patrollRange.look_at(0)
            elif self.move == NE:
                self.patrollRange.look_at(math.radians(45))
            elif self.move == N:
                self.patrollRange.look_at(math.radians(90))
            elif self.move == NW:
                self.patrollRange.look_at(math.radians(135))
            elif self.move == W:
                self.patrollRange.look_at(math.radians(180))
            elif self.move == SW:
                self.patrollRange.look_at(math.radians(225))
            elif self.move == S or self.move == STILL:
                self.patrollRange.look_at(math.radians(270))
            elif self.move == SE:
                self.patrollRange.look_at(math.radians(315))

        # Compruebo si el jugador está en el rango de visión
        self.playerCollision = pygame.sprite.collide_mask(self.patrollRange, player)

    def update(self, enemy, time, mapRect, mapMask):
        # Actualizamos el delay
        self.delay -= time

        # Si el jugador está en mi rango de visión, compruebo que no haya una pared antes
        if self.playerCollision is not None:
            # Obtengo las posiciones del mapa y del enemigo
            (enemyX, enemyY) = self.patrollRange.rect.topleft
            (mapX, mapY) = mapRect.topleft
            # Offset entre la máscara y el mapa
            offset = (mapX-enemyX, mapY-enemyY)
            # Creo una copia de la máscara del mapa y la invierto (Si no, no
            # funciona)
            invertMap = pygame.mask.Mask(mapMask.get_size())
            invertMap.draw(mapMask, (0, 0))
            invertMap.invert()
            # Obtengo el punto de colisión de la máscara
            mapCollision = self.patrollRange.mask.overlap(invertMap, offset)
            # Obtengo la distancia del jugador a la máscara
            distPlayer = math.hypot(self.playerCollision[0], self.playerCollision[1])
            distMap = sys.maxint
            # Si hay colisión obtengo la distancia del mapa a la máscara
            if mapCollision is not None:
                distMap = math.hypot(mapCollision[0], mapCollision[1])
            # Si está antes es que veo al enemigo
            if distPlayer < distMap:
                self.count += 1
                print "He visto al enemigo", self.count # TODO Cambiar el estado

        # Actualizamos el enemigo
        Character.update(enemy, time, mapRect, mapMask)

        # Actualizamos la posición de la máscara
        self.patrollRange.rect.center = enemy.rect.center
        self.patrollRange.position = enemy.rect.bottomleft
