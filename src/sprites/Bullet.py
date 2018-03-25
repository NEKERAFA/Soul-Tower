# -*- coding: utf-8 -*-

import pygame, sys, os, math
from src.sprites.MySprite import *
from src.sprites.Attack import *

BASE_SPEED = 0.1
# -------------------------------------------------
# Clase del proyectil

class Bullet(MySprite):
    def __init__(self, characterPos, rotation, radius, frameImage, frameRect):
        # Llamamos a la superclase
        MySprite.__init__(self)

        # Guardamos la posición y el rectangulo
        self.image = frameImage.copy()
        self.rect = frameRect.copy()

        # Lo ponemos en posición
        width, height = self.image.get_size()
        x, y = Attack.calc_rot_pos(rotation, radius, self.rect.width, self.rect.height, characterPos)
        self.position = (x, y)
        self.rect.top = self.position[0]
        self.rect.left = self.position[1]
        self.image = pygame.transform.rotate(self.image, rotation)
        self.speed = (BASE_SPEED * (math.cos(math.radians(rotation))), -BASE_SPEED * (math.sin(math.radians(rotation))))
        self.rotation = rotation

    def update (self, time, mapMask, frameImage, frameMask, frameRect):
        # Actualizamos el frame
        self.image = pygame.transform.rotate(frameImage, self.rotation)
        center = self.rect.center
        self.rect = frameRect.copy()
        self.rect.center = center
        # Actualizamos la posición
        MySprite.update(self, time)
        # Comprobamos si ha chocado con la pared para eliminarla de todos los
        # grupos a los que esté asociada la bala
        x, y = self.rect.topleft
        if frameMask.overlap(mapMask, (-x, -y)) is not None:
            self.kill()
