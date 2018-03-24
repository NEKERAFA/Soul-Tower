# -*- coding: utf-8 -*-

import pygame, sys, os, math
from src.sprites.Attack import *

# -------------------------------------------------
# Sprites de ataques
class MeleeAttack(Attack):
    def __init__(self, imageFile, spriteSheet, radius, delayTime, enemies):
        # Primero invocamos al constructor de la clase padre
        Attack.__init__(self, imageFile, spriteSheet, enemies)
        self.delayTime = delayTime
        self.elapsedTime = 0
        self.radius = radius
        self.attacking = False

    def start_attack(self, characterPos, rotation):
        self.attacking = True
        self.position = Attack.calc_rot_pos(rotation, self.radius, self.rect.width, self.rect.height, characterPos)
        self.rect.left = self.position[0]
        self.rect.top = self.position[1]
        self.image = pygame.transform.rotate(self.origImage, rotation)

    def end_attack(self):
        self.attacking = False

    def update(self, time):
        # Si ha pasado el tiempo suficiente y estamos intentando atacar
        if (self.elapsedTime > self.delayTime) and self.attacking:
            self.drawAnimation = True
            # Y reiniciar el contador
            self.elapsedTime = 0
        else:
            self.elapsedTime += time

        Attack.update(self, time)
