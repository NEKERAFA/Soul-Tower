# -*- coding: utf-8 -*-

import pygame, random
from src.sprites.characters.behaviours.BehaviourState import *
from src.sprites.Character import *

# ------------------------------------------------------------------------------
# Clase WanderingState

# TODO Ajustar aquí
MAX_DELAY = 2000
MIN_DELAY = 500

MOVEMENTS = [N, NW, W, SW, S, SE, E, NE]

class WanderingState(BehaviourState):
    def __init__(self):
        # Llamamos al constructor de la superclase
        BehaviourState.__init__(self)
        # Empieza parado y con un tiempo random
        self.move = STILL
        self.delay = random.randint(MIN_DELAY, MAX_DELAY)

    def move_ai(self, enemy, player):
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

            # Se mueve
            Character.move(enemy, self.move)

    def update(self, enemy, time, mapRect, mapMask):
        # Actualizamos el delay
        self.delay -= time
        oldPosition = enemy.position
        # Llamamos al update de characters
        Character.update(enemy, time, mapRect, mapMask)
        # Esto es para que no se salga de la sala
        if not mapRect.inflate(-12, -12).contains(enemy.rect):
            # Miramos a donde nos tenemos que mover
            if enemy.rect.top < mapRect.top+6:
                # Choca arriba
                if enemy.rect.left < mapRect.left+6:
                    # Choca arriba a la izquierda
                    Character.move(enemy, SW)
                elif enemy.rect.right > mapRect.right-6:
                    # Choca arriba a la derecha
                    Character.move(enemy, SE)
                else:
                    Character.move(enemy, random.choice([SW, SE, S]))
            elif enemy.rect.bottom > mapRect.bottom-6:
                # Choca abajo
                if enemy.rect.left < mapRect.left+6:
                    # Choca abajo a la izquierda
                    Character.move(enemy, NW)
                elif enemy.rect.right > mapRect.right-6:
                    # Choca abajo a la derecha
                    Character.move(enemy, NE)
                else:
                    Character.move(enemy, random.choice([NW, NE, N]))
            # Choca a la izquierda
            elif enemy.rect.left < mapRect.left+6:
                Character.move(enemy, random.choice([NE, E, SE]))
            # Choca a la derecha
            elif enemy.rect.right > mapRect.right-6:
                Character.move(enemy, random.choice([SW, W, NW]))
            else:
                print "No se que hacer"
                self.angle = random.randint(0, 356)    
            # Volvemos a la posición anterior
            enemy.change_global_position(oldPosition)
            # Tiempo aleatorio
            self.delay = random.randint(MIN_DELAY, MAX_DELAY)
