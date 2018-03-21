# -*- coding: utf-8 -*-

import pygame, sys, os
from pygame.locals import *
from src.sprites.Character import *
from src.sprites.characters.player.PlayerState import *
from src.sprites.characters.player.Normal import *
from src.sprites.characters.player.Dashing import *
from src.sprites.characters.player.Defending import *
from src.sprites.attacks.MeleeAttack import *
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
    def __init__(self, enemies):
        # Invocamos al constructor de la clase padre con la configuracion de este Character concreto
        Character.__init__(self, 'sorcerer')
        self.controlManager = KeyboardMouseControl()

        # Atributo de estado del jugador (patrón estado)
        self.playerState = Normal()

        # Se carga el ataque a melee
        self.meleeAttack = MeleeAttack('sprites/characters/sorcerer.png', 'attacks/attack.json', 30, 250, enemies)
        # Número de almas
        self.souls = 0

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

        # Cambios de estado
        # Si está dasheando:
        if self.controlManager.sec_button():
            self.playerState.change(self, Dashing)
        
        # control de ataque
        if self.controlManager.prim_button():
            # calcular la posición del centro del sprite (de momento calcula el centro del primer sprite)
            #center_pos = (self.position[0]+self.offset[0],self.position[1]-self.offset[1])
            centerPosX, centerPosY = self.rect.center
            centerPosX -= viewport.left
            centerPosY -= viewport.top
            centerPos = centerPosX,centerPosY
            # print(centerPos)
            # print(center_pos)
            self.meleeAttack.start_attack(centerPos, self.controlManager.angle(centerPos))
        else:
            self.meleeAttack.end_attack()

    def update(self, time, mapRect, mapMask):
        # Delegamos en el estado del jugador para actualizar
        print(self.stats["nrg"])
        self.playerState.update_state(self, time, mapRect, mapMask)
        self.meleeAttack.update(time)

    ############################################################################

    # Incrementa el número de almas del jugador
    def increase_souls(self, souls):
        self.souls += souls
        print(self.souls)
