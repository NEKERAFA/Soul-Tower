# -*- coding: utf-8 -*-

import pygame, sys, os
from pygame.locals import *

# Sprites en general
class MySprite(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.position = (0, 0)
        self.speed = (0, 0)
        self.scroll = (0, 0)

    # Cambia la posición en el mundo
    def change_global_position(self, position):
        self.position = position
        self.rect.left = self.position[0] - self.scroll[0]
        self.rect.bottom = self.position[1] - self.scroll[1]

    # Cambia la posición solamente en la pantalla
    def change_screen_position(self, scroll):
        self.scroll = scroll;
        (scrollX, scrollY) = self.scroll;
        (posX, posY) = self.position;
        self.rect.left = posX - scrollX;
        self.rect.bottom = posY - scrollY;

    def increment_position(self, increment):
        (posX, posY) = self.position
        (incrementX, incrementY) = increment
        self.change_global_position((posX+incrementX, posY+incrementY))

    def update(self, time):
        incrementX = self.speed[0]*time
        incrementY = self.speed[1]*time
        self.increment_position((incrementX, incrementY))
