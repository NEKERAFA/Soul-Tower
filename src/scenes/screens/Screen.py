# -*- coding: utf-8 -*-

import pygame
from src.ResourceManager import *
from src.scenes.Scene import *

# -------------------------------------------------
# Clase Screen
# TODO: maybe hacer que GUIScreen y Screen hereden de la misma clase (¿una "superscreen"?)

class Screen(object):
    def __init__(self, pathImage):
        self.image = ResourceManager.load_image(pathImage, (255, 0, 255))

    def update(self, scroll):
        pass

    def draw(self, screen):
        self.blit(self.image, (0, 0))
