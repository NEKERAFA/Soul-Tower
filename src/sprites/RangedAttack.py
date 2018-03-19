# -*- coding: utf-8 -*-

import pygame, sys, os, math
from src.sprites.Bullet import *

# -------------------------------------------------
# Sprites de ataques
class RangedAttack(object):
    def __init__(self, imageFile, spriteSheet, radius, delayTime, enemyGroup, stage):
        # Primero invocamos al constructor de la clase padre
        self.imageFile = imageFile
        self.spriteSheet = spriteSheet
        self.radius = radius
        self.enemyGroup = enemyGroup
        self.delayTime = delayTime
        self.elapsedTime = 0
        self.radius = radius
        self.attacking = False
        # self.bullets = []
        self.stage = stage

    def start_attack(self, characterPos, rotation):
        self.characterPos = characterPos
        self.rotation = rotation
        self.attacking = True

    def end_attack(self):
        self.attacking = False

    # def draw(self, surface):
    #     for bullet in self.bullets:
    #         bullet.draw(surface)

    def update(self, time):
        # Si ha pasado el tiempo suficiente y estamos intentando atacar
        if (self.elapsedTime > self.delayTime) and self.attacking:
            bullet = Bullet(self.imageFile, self.spriteSheet, self.enemyGroup, self.characterPos, self.rotation, self.radius)
            self.stage.bulletGroup.add(bullet)
            # self.bullets.append(bullet)
            # self.drawAnimation = True
            # Y reiniciar el contador
            self.elapsedTime = 0
        else:
            self.elapsedTime += time

        # for bullet in self.bullets:
        #     bullet.update(time)
        # Attack.update(self, time)
