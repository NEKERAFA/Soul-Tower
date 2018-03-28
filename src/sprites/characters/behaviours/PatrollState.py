# -*- coding: utf-8 -*-

import pygame, random, math, sys
from src.sprites.characters.behaviours.BehaviourState import *
from src.sprites.Character import *
from src.sprites.EnemyRange import *

# ------------------------------------------------------------------------------
# Clase PatrollState

# TODO Ajustar aquí
MAX_DELAY = 2000
MIN_DELAY = 500

MOVEMENTS = [N, NW, W, SW, S, SE, E, NE]

class PatrollState(BehaviourState):
    def __init__(self, center, radius, vision, move=STILL):
        # Llamamos al constructor de la superclase
        BehaviourState.__init__(self)

        # Empieza parado y con un tiempo random
        self.move = move
        self.delay = random.randint(MIN_DELAY, MAX_DELAY)

        # Creo el rango de vision
        self.range = EnemyRange(center, radius, vision, EnemyRange.get_angle(move))

        # Inicializo los valores de la distancia del jugador
        self.playerCollision = None
        self.playerDistance = sys.maxint

    def move_ai(self, enemy, player):
        # Comprobamos si hay colisión con el jugador en el rango de visión
        self.playerCollision = pygame.sprite.collide_mask(self.range, player)

        # Convierto el punto de colisión para dejarlo con el centro en el
        # enemigo
        if self.playerCollision is not None:
            deltaX, deltaY = self.range.get_delta()
            self.playerCollision = (self.playerCollision[0]-deltaX, self.playerCollision[1]-deltaY)

            # Distancia al jugador
            self.playerDistance = math.hypot(self.playerCollision[0], self.playerCollision[1])
        else:
            self.playerDistance = sys.maxint

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
            self.range.look_at(EnemyRange.get_angle(self.move))

    def update(self, enemy, time, mapRect, mapMask):
        # Actualizamos el delay
        self.delay -= time

        # Si hay colisión con el jugador, comprobamos si hay colisión con el
        # mapa de la fase
        if self.playerCollision is not None:
            # Creo una imagen con una linea para saber en que punto colisiona
            size = (self.range.radius*2, self.range.radius*2)
            line = pygame.Surface(size)
            center = (self.range.radius, self.range.radius)
            end = (self.playerCollision[0]+self.range.radius, self.playerCollision[1]+self.range.radius)
            pygame.draw.line(line, (0, 0, 255), center, end, 1)
            line.set_colorkey((0, 0, 0))

            # Creo la máscara para comprobar colisión con el mapa
            raytestMask = pygame.mask.from_surface(line)

            # Obtengo el offset
            x = enemy.rect.centerx-self.range.radius
            y = enemy.rect.centery-self.range.radius

            # Colisión con el mapa
            stageCollision = raytestMask.overlap(mapMask, (-x, -y))

            # Distancia al mapa infinita
            stageDistance = sys.maxint

            # Obtengo la distancia real si hay colisión
            if stageCollision is not None:
                stageCollision = (stageCollision[0]-self.range.radius, stageCollision[1]-self.range.radius)
                stageDistance = math.hypot(stageCollision[0], stageCollision[1])

            # Si la colisión del jugador está a menor distancia con la colisión
            # contra la pared, es que está delante de la pared
            if self.playerDistance <= stageDistance:
                # Creamos el estado de seguir
                enemy.state = FollowPlayerState(self.range.radius, self.range.angle, enemy.movement)

                # Ejecutamos el nuevo estado
                enemy.state.update(enemy, time, mapRect, mapMask)
                return

        # Llamamos al update de characters
        Character.update(enemy, time, mapRect, mapMask)

        # Actualizamos la posición del campo de visión
        (enemyX, enemyY) = enemy.rect.center
        (rangeX, rangeY) = self.range.rect.center
        self.range.increment_position((enemyX-rangeX, enemyY-rangeY))

# Se pone aquí debido al import recursivo
from src.sprites.characters.behaviours.FollowPlayerState import FollowPlayerState
