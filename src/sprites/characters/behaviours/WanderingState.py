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
        # Llamamos al update de characters
        Character.update(enemy, time, mapRect, mapMask)
