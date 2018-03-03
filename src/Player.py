# -*- coding: utf-8 -*-

import pygame, sys, os
from pygame.locals import *
from Character import *

# -------------------------------------------------
# -------------------------------------------------
# Constantes
# -------------------------------------------------
# -------------------------------------------------

# movimientos
STILL = 0
W = 1
E = 2
N = 3
S = 4
NW = 5
NE = 6
SW = 7
SE = 8

PLAYER_SPEED = 0.25 # Pixeles por milisegundo
PLAYER_ANIMATION_DELAY = 5 # updates que durará cada imagen del Character
                # debería de ser un valor distinto para cada postura
# -------------------------------------------------
# Clase del Character jugable
class Player(Character):
    def __init__(self):
        # Invocamos al constructor de la clase padre con la configuracion de este Character concreto
        Character.__init__(self,'Jugador.png','coordJugador.txt', [6, 12, 6], PLAYER_SPEED, PLAYER_ANIMATION_DELAY);
        self.controlManager = KeyboardMouseControl()
        # para obtener el width y height de la animación en reposo
        width = self.sheetCoords[0][0][2]
        height = self.sheetCoords[0][0][3]
        # con ello calcular el offset al centro de la imagen
        self.offset = (int(width/2),int(height/2))

    def move(self):
        # Indicamos la acción a realizar segun la tecla pulsada para el jugador
        if self.controlManager.left():
            if self.controlManager.up():
                Character.move(self,NW)
            elif self.controlManager.down():
                Character.move(self,SW)
            else:
                Character.move(self,W)
        elif self.controlManager.right():
            if self.controlManager.up():
                Character.move(self,NE)
            elif self.controlManager.down():
                Character.move(self,SE)
            else:
                Character.move(self,E)
        elif self.controlManager.up():
            Character.move(self,N)
        elif self.controlManager.down():
            Character.move(self,S)
        else:
            Character.move(self,STILL)
        