# -*- coding: utf-8 -*-

import pygame, sys, os, math
from src.sprites.Attack import *

# -------------------------------------------------
# Sprites de ataques
class MeleeAttack(Attack):
    def __init__(self, imageFile, spriteSheet, radius, delayTime, enemyGroup):
        # Primero invocamos al constructor de la clase padre
        Attack.__init__(self, imageFile, spriteSheet, enemyGroup)
        self.delayTime = delayTime
        self.elapsedTime = 0
        self.radius = radius
        self.attacking = False

    def startAttack(self, characterPos, rotation):
        self.attacking = True
        self.position = Attack.calcRotPos(rotation, self.radius, self.width, self.height, characterPos)
        self.rect.left = self.position[0]
        self.rect.top = self.position[1]
        self.image = pygame.transform.rotate(self.origImage, rotation)

    def endAttack(self):
        self.attacking = False

    def update(self, time):
        #print(self.elapsedTime, self.delayTime, self.attacking, self.drawAnimation)

        # Si ha pasado el tiempo suficiente y estamos intentando atacar
        if (self.elapsedTime > self.delayTime) and self.attacking:
            self.drawAnimation = True
            # Y reiniciar el contador
            self.elapsedTime = 0
        else:
            self.elapsedTime += time

        Attack.update(self, time)
