# -*- coding: utf-8 -*-

import pygame, sys, os, math
from src.sprites.Attack import *

# -------------------------------------------------
# Sprites de ataques
class MeleeAttack(Attack):
    def __init__(self, radius, delayTime, enemies):
        # Obtenemos las rutas a los archivos
        imageFile = os.path.join('sprites', 'attacks', 'melee.png')
        spriteSheet = os.path.join('attacks', 'melee.json')

        # Invocamos al constructor de la clase padre
        Attack.__init__(self, imageFile, spriteSheet, enemies)

        # Tiempo entre ataques melee
        self.delayTime = delayTime
        self.elapsedTime = 0
        # Radio del ataque
        self.radius = radius
        # Comprueba si está atacando
        self.attacking = False

    def start_attack(self, characterPos, rotation):
        self.attacking = True
        self.position = Attack.calc_rot_pos(rotation, self.radius, self.rect.width, self.rect.height, characterPos)
        self.rect.left = self.position[0]
        self.rect.top = self.position[1]
        self.rotation = rotation

    def end_attack(self):
        self.attacking = False

    def update(self, time, stage):
        # Si ha pasado el tiempo suficiente y estamos intentando atacar
        if (self.elapsedTime > self.delayTime) and self.attacking:
            self.drawAnimation = True
            # Y reiniciar el contador
            self.elapsedTime = 0
        else:
            self.elapsedTime += time

        Attack.update(self, time)

        if self.drawAnimation:
            if self.rotation >= 90:
                self.image = pygame.transform.rotate(self.origImage, 180-self.rotation)
                self.image = pygame.transform.flip(self.image, True, False)
            elif self.rotation <= -90:
                self.image = pygame.transform.rotate(self.origImage, -180-self.rotation)
                self.image = pygame.transform.flip(self.image, True, False)
            else:
                self.image = pygame.transform.rotate(self.origImage, self.rotation)
