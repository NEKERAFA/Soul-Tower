# -*- coding: utf-8 -*-

import pygame
from src.ResourceManager import *
from src.scenes.Scene import *

# -------------------------------------------------
# Clase Screen

class Screen(object):
    def __init__(self, path_image):
        self.image = ResourceManager.load_image(path_image, (255, 0, 255))

    def update(self, scroll):
        pass

    def draw(self, screen):
        self.blit(self.image, (0, 0))
