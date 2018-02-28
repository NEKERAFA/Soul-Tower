# -*- coding: utf-8 -*-

import pygame, sys, os

from pygame.locals import *

# -------------------------------------------------
# Clase MySprite

class MySprite(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.position = (0, 0)
        self.velocity = (0, 0)
        self.scroll   = (0, 0)

    def set_position(self, position):
        self.position = position
        self.rect.left = self.position[0] - self.scroll[0]
        self.rect.bottom = self.position[1] - self.scroll[1]

    def set_position_screen(self, scroll):
        self.scroll = scroll;
        (scrollX, scrollY) = scroll;
        (posX, posY) = self.position;
        self.rect.left = posX - scrollX;
        self.rect.bottom = posY - scrollY;

    def move(self, increment):
        (posX, posY) = self.position
        (incX, incY) = increment
        self.set_position((posX+incX, posY+incY))

    def update(self, time):
        incX = self.velocity[0] * time
        incY = self.velocity[1] * time
        self.add_position((incX, incY))
