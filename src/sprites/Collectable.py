# -*- coding: utf-8 -*-

import pygame

# Con esta clase me aseguro de que haya ciertos elementos que se puedan recoger

class Collectable(object):
    def collect(self, stage):
        raise NotImplementedError('Error: implemente el método activate')

    def collide(self, character):
        return character.rect.colliderect(self.collision)
