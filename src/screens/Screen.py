# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
from src.ResourceManager import *

# -------------------------------------------------
# Clase screens

class Screen(object):
    def __init__(self, path_image):
        self.image = ResourceManager.load_image(path_image, -1)
        self.x = 0
        self.y = 0

    def events(self, list_events):
        pass

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
