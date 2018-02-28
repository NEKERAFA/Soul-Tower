# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
from src.ResourceManager import *

# -------------------------------------------------
# Clase screens

class Screen(object):
    def __init__(self, path_image):
        self.image = ResourceManager.load_image(path_image)

    def events(self, list_events):
        pass

    def draw(self, screen):
        self.image.blit(screen, (0, 0))
