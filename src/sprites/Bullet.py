# -*- coding: utf-8 -*-

import pygame, sys, os, math
from src.sprites.Attack import *

BASE_SPEED = 0.1
# -------------------------------------------------
# Clase del proyectil

class Bullet(Attack):

    def __init__(self, imageFile, spriteSheet, enemyGroup, characterPos, rotation, radius):
        #TODO:Pasar el angulo a velocidad (tenemos en cuenta el signo del angulo)
        Attack.__init__(self, imageFile, spriteSheet, enemyGroup)
        # self.image = sheet.subsurface(sheetCoords[0][0])
        # self.rect = self.image.get_rect(center=pos)
        # self.position = pos
        # self.rotation = rotation
        self.position = Attack.calc_rot_pos(rotation, radius, self.rect.width, self.rect.height, characterPos)
        self.rect.left = self.position[0]
        self.rect.top = self.position[1]
        self.image = pygame.transform.rotate(self.origImage, rotation)
        self.speed = (BASE_SPEED * (math.cos(math.radians(rotation))),-BASE_SPEED * (math.sin(math.radians(rotation))))
        print(self.position, 'ranged')

    def draw(self, surface):
        Attack.draw(self, surface)

    def update (self, time):
        self.drawAnimation = True
        Attack.update(self, time)
        MySprite.update(self, time)
        # print(self.drawAnimation)
        # print(self.position)
        # comprobar colisiones contra paredes y eliminar la bala
