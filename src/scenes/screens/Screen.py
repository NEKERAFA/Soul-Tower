# -*- coding: utf-8 -*-

import pygame
from src.ResourceManager import *
from src.scenes.Scene import *

# -------------------------------------------------
# Clase Screen

class Screen(object):
    def __init__(self, path_image):
        self.image = ResourceManager.load_image(path_image, -1)
        self.rect = self.image.get_rect()
        self.subRect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

    def update(self, scroll):
        self.subRect.left = scroll

    def draw(self, screen):
        screen.blit(self.image, self.rect, self.subRect)
