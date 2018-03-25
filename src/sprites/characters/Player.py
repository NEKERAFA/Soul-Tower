# -*- coding: utf-8 -*-

import pygame, sys, os
from pygame.locals import *
from src.sprites.Character import *
from src.sprites.characters.player.specials.Normal import *
from src.sprites.characters.player.specials.Dashing import *
from src.sprites.characters.player.specials.Defending import *
from src.sprites.characters.player.changing.Finish import *
from src.sprites.attacks.MeleeAttack import *
from src.sprites.attacks.RangedAttack import *
from src.controls.KeyboardMouseControl import *
from src.ResourceManager import *

# -------------------------------------------------
# -------------------------------------------------
# Constantes
# -------------------------------------------------
# -------------------------------------------------

PLAYER_SPEED = 0.2 # Pixeles por milisegundo

# -------------------------------------------------
# Clase del Character jugable
class Player(Character):
    def __init__(self, enemies, stage):
        # Invocamos al constructor de la clase padre con la configuracion de este Character concreto
        Character.__init__(self, 'sorcerer')

        # Rutas de las sprite sheets del personaje principal
        sorcererPath = os.path.join('sprites', 'characters', 'sorcerer.png')
        warriorPath = os.path.join('sprites', 'characters', 'warrior.png')

        # Cargamos las sprite sheets
        self.sorcererSheet = ResourceManager.load_image(sorcererPath, (-1))
        self.warriorSheet = ResourceManager.load_image(warriorPath, (-1))

        # Atributo de estado del jugador (patrón estado)
        self.state = Normal()

        # Se cargan los ataques
        self.attack = RangedAttack(15, 250, enemies)

        # Número de almas
        self.souls = 0

        # Esta variable mira si se puede cambiar de personaje o no
        self.canChange = True

        # Personaje activo en este momento
        self.currentCharacter = 'sorcerer'

        # Si se está cambiando de personaje o no
        self.changing = Finish()

    def move(self, viewport):
        # Indicamos la acción a realizar segun la tecla pulsada para el jugador
        if KeyboardMouseControl.left():
            if KeyboardMouseControl.up():
                Character.move(self, NW)
            elif KeyboardMouseControl.down():
                Character.move(self, SW)
            else:
                Character.move(self, W)
        elif KeyboardMouseControl.right():
            if KeyboardMouseControl.up():
                Character.move(self, NE)
            elif KeyboardMouseControl.down():
                Character.move(self, SE)
            else:
                Character.move(self, E)
        elif KeyboardMouseControl.up():
            Character.move(self, N)
        elif KeyboardMouseControl.down():
            Character.move(self, S)
        else:
            Character.move(self, STILL)

        # Control de ataque
        if KeyboardMouseControl.prim_button():
            # Si es sorcerer, el ataque actual es ataque a distancia
            if self.currentCharacter == 'sorcerer' and type(self.attack) is not RangedAttack:
                self.attack = RangedAttack(15, 250, self.attack.enemies)

            # Si es warrior, el ataque actual es melee
            if self.currentCharacter == 'warrior' and type(self.attack) is not MeleeAttack:
                self.attack = MeleeAttack(15, 500, self.attack.enemies)

            # Calcular la posición del centro del sprite (de momento calcula el centro del primer sprite)
            centerPosX, centerPosY = self.rect.center
            centerPosX -= viewport.left
            centerPosY -= viewport.top
            centerPos = centerPosX, centerPosY
            self.attack.start_attack(self.rect.center, KeyboardMouseControl.angle(centerPos))
        # Finalizamos el ataque
        else:
            self.attack.end_attack()

    def update(self, time, mapRect, mapMask):
        # Ataque especial
        if KeyboardMouseControl.sec_button():
            # Si es sorcerer el jugador actual, cambiamos el estado a dashing
            if self.currentCharacter == 'sorcerer':
                self.state.change(Dashing)

            if self.currentCharacter == 'warrior':
                self.state.change(Dashing) # TODO cambiar

        # Controlamos el cambio de personaje
        self.changing.update(self, time, mapRect, mapMask)

    def draw(self, screen):
        # Esta función está para agrupar el mostrar al jugador y su ataque
        screen.blit(self.image, self.rect)

        if hasattr(self.attack, 'draw'):
            self.attack.draw(screen)

    ############################################################################

    # Incrementa el número de almas del jugador
    def increase_souls(self, souls):
        self.souls += souls
        print(self.souls)

    # Recibe un daño y se realiza el daño. Si el personaje ha muerto, lo elimina
    # de todos los grupos
    def receive_damage(self, damage, angle):
        if type(self.state) is Normal:
            Character.receive_damage(self, damage, angle)
