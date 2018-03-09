# -*- coding: utf-8 -*-

import pygame, sys, os
from pygame.locals import *
from src.sprites.Character import *

# -------------------------------------------------
# -------------------------------------------------
# Constantes
# -------------------------------------------------
# -------------------------------------------------

PLAYER_SPEED = 0.2 # Pixeles por milisegundo

# -------------------------------------------------
# Clase del Character jugable
class Player(Character):
    def __init__(self):
        # Invocamos al constructor de la clase padre con la configuracion de este Character concreto
        Character.__init__(self, 'characters/bee_1.png', 'bee.json', PLAYER_SPEED)
        self.controlManager = KeyboardMouseControl()
        # para obtener el width y height de la animación en reposo
        width = self.sheetConf[0][0]['coords'][2]
        height = self.sheetConf[0][0]['coords'][3]
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

        # control de ataque
        if self.controlManager.primButton():
            # calcular la posición del centro del sprite (de momento calcula el centro del primer sprite)
            center_pos = (self.position[0]+self.offset[0],self.position[1]-self.offset[1])
            self.melee_manager.startAttack(center_pos, self.controlManager.angle(center_pos))
        else:
            self.melee_manager.endAttack()
