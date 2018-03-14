# -*- coding: utf-8 -*-

import pygame, sys, os
from pygame.locals import *
from src.sprites.Character import *
# from src.sprites.MeleeAttack import *
from src.controls.KeyboardMouseControl import *

# -------------------------------------------------
# -------------------------------------------------
# Constantes
# -------------------------------------------------
# -------------------------------------------------

PLAYER_SPEED = 0.2 # Pixeles por milisegundo

# -------------------------------------------------
# Clase del Character jugable
class Player(Character):
    def __init__(self):#, enemies):
        # Invocamos al constructor de la clase padre con la configuracion de este Character concreto
        Character.__init__(self, 'sorcerer')
        self.controlManager = KeyboardMouseControl()
        # con ello calcular el offset al centro de la imagen
        # self.offset = (int(self.width/2), int(self.height/2))
        # self.meleeAttack = MeleeAttack('characters/sorcerer.png', 'attack.json', 30, 250, enemies)

    def move(self, viewport):
        # Indicamos la acción a realizar segun la tecla pulsada para el jugador
        if self.controlManager.left():
            if self.controlManager.up():
                Character.move(self, NW)
            elif self.controlManager.down():
                Character.move(self, SW)
            else:
                Character.move(self, W)
        elif self.controlManager.right():
            if self.controlManager.up():
                Character.move(self, NE)
            elif self.controlManager.down():
                Character.move(self, SE)
            else:
                Character.move(self, E)
        elif self.controlManager.up():
            Character.move(self, N)
        elif self.controlManager.down():
            Character.move(self, S)
        else:
            Character.move(self, STILL)

        # control de ataque
        # if self.controlManager.prim_button():
        #     # calcular la posición del centro del sprite (de momento calcula el centro del primer sprite)
        #     #center_pos = (self.position[0]+self.offset[0],self.position[1]-self.offset[1])
        #     centerPosX, centerPosY = self.rect.center
        #     centerPosX -= viewport.left
        #     centerPosY -= viewport.top
        #     centerPos = centerPosX,centerPosY
        #     # print(centerPos)
        #     # print(center_pos)
        #     self.meleeAttack.start_attack(centerPos, self.controlManager.angle(centerPos))
        # else:
        #     self.meleeAttack.end_attack()

    def update(self, mapRect, mapMask, time):
        Character.update(self, mapRect, mapMask, time)
        # self.meleeAttack.update(time)
