# -*- coding: utf-8 -*-

import pygame, sys, os, math
from src.sprites.MySprite import *
from src.sprites.Attack import *

BASE_SPEED = 0.25
# -------------------------------------------------
# Clase del proyectil

class Bullet(MySprite):
    def __init__(self, characterPos, rotation, radius, frameImage, baseSpeed=None):
        # Llamamos a la superclase
        MySprite.__init__(self)
        # Rotamos la imagen
        self.image = pygame.transform.rotate(frameImage, rotation)
        width = frameImage.get_rect().width
        height = frameImage.get_rect().height

        # Obtenemos la posición
        x, y = Attack.calc_rot_pos(rotation, radius, width, height, characterPos)
        # Lo ponemos en el centro
        self.position = (x, y+height)
        self.rect = pygame.Rect((x, y), (width, height))
        self.baseSpeed = baseSpeed if baseSpeed is not None else BASE_SPEED
        self.speed = (self.baseSpeed * (math.cos(math.radians(rotation))), - self.baseSpeed * (math.sin(math.radians(rotation))))
        self.rotation = rotation

    def update(self, time, stage, frameImage):
        # Actualizamos el frame
        self.image = pygame.transform.rotate(frameImage, self.rotation)
        # Actualizamos la posición
        MySprite.update(self, time)
        # Comprobamos si ha chocado con la pared para eliminarla de todos los
        # grupos a los que esté asociada la bala
        x, y = self.rect.topleft
        mask = pygame.mask.from_surface(self.image)
        if not stage.viewport.contains(self.rect) or mask.overlap(stage.rangedMask, (-x, -y)):
            self.kill()
