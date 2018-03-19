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
    def __init__(self, center, radius, vision):
        # Llamamos al constructor de la superclase
        BehaviourState.__init__(self)
        # Empieza parado y con un tiempo random
        self.move = STILL
        self.delay = random.randint(MIN_DELAY, MAX_DELAY)
        # Creo el rango de vision
        self.range = EnemyRange(radius, vision, 270)
        self.range.rect.center = center
        self.playerCollision = None

    def move_ai(self, enemy, player):
        # Comprobamos si hay colisión con el jugador en el rango de visión
        self.playerCollision = pygame.sprite.collide_mask(self.range, player)

        # Si se acaba el tiempo, cambia el movimiento
        if self.delay <= 0:
            # Si estaba pausado, se mueve
            if self.move == STILL:
                self.move = random.choice(MOVEMENTS)
            # Si se estaba moviendo, se pausa
            else:
                self.move = STILL
            # Tiempo aleatorio
            self.delay = random.randint(MIN_DELAY, MAX_DELAY)
            # Se actualiza la posición del jugador
            Character.move(enemy, self.move)
            # Se rota el rango de visión
            if self.move == E:
                self.range.look_at(0)
            elif self.move == NE:
                self.range.look_at(45)
            elif self.move == N:
                self.range.look_at(90)
            elif self.move == NW:
                self.range.look_at(135)
            elif self.move == W:
                self.range.look_at(180)
            elif self.move == SW:
                self.range.look_at(225)
            elif self.move == S or self.move == STILL:
                self.range.look_at(270)
            elif self.move == SE:
                self.range.look_at(315)

    def update(self, enemy, time, mapRect, mapMask):
        # Actualizamos el delay
        self.delay -= time

        # Si hay colisión con el jugador, comprobamos si hay colisión con el
        # mapa de la fase
        if self.playerCollision is not None:
            # Calculo el delta del centro de vision
            (posX, posY) = self.range.rect.topleft
            (centerX, centerY) = self.range.rect.center
            deltaX, deltaY = centerX-posX, centerY-posY
            # Colisión con el mapa
            stageCollision = self.range.mask.overlap(mapMask, (-posX, -posY))
            # Distancia con el jugador
            distPlayer = math.hypot(self.playerCollision[0]-deltaX, self.playerCollision[1]-deltaY)
            # Distancia con el mapa
            distStage = sys.maxint
            if stageCollision is not None:
                distStage = math.hypot(stageCollision[0]-deltaX, stageCollision[1]-deltaY)
            # Si la colisión del jugador está a menor distancia, es que está delante de la pared
            if distPlayer <= distStage:
                print "Veo al jugador"
                # Creamos el estado de seguir
                enemy.state = FollowPlayerState(enemy.rect.center, self.range.radius, self.range.angle)
                # Establezcemos la dirección a donde mira
                enemy.state.range.look_at(self.range.lookAt)
                # Ejecutamos el nuevo estado
                enemy.state.update(enemy, time, mapRect, mapMask)

        # Llamamos al update de characters
        Character.update(enemy, time, mapRect, mapMask)

        # Actualizamos la posición del campo de visión
        (enemyX, enemyY) = enemy.rect.center
        (rangeX, rangeY) = self.range.rect.center
        self.range.increment_position((enemyX-rangeX, enemyY-rangeY))


from src.sprites.behaviours.FollowPlayerState import FollowPlayerState
