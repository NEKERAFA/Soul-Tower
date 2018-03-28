# -*- coding: utf-8 -*-

import pygame

# Con esta clase me aseguro de que haya ciertos elementos que se puedan activar
# o interactuar con ellos

class Interactive(object):
    def __init__(self, collision):
        self.collision = collision

    def activate(self):
        raise NotImplementedError('Error: implemente el método activate')

    def collide(self, character):
        return character.rect.colliderect(self.collision)
