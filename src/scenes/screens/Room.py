# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
from src.ResourceManager import *
from src.scenes.screens.Screen import *

# -------------------------------------------------
# Clase Room

class Room(Screen):
    def __init__(self, map_file, mask_file, room_file):
        # Llamamos al constructor de la clase superior
        Screen.__init__(self, map_file)
        self.rect = self.image.get_rect()
        self.subRect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

        # Llamamos al ResourceManager para cargar la mascara del mapa
        self.mask = ResourceManager.load_image(mask_file, -1)
        self.mask = pygame.mask.from_surface(self.mask, 127)

        # Llamamos al ResourceManager para cargar el mapa
        data = ResourceManager.load_room(room_file)
        self.rect.left = data["x"]
        self.x = data["x"]
        self.y = data["y"]
        self.width = data["width"]
        self.height = data["height"]
        self.connections = data["connections"]

    def update(self, scroll):
        self.subRect.left = scroll[0]

    def draw(self, screen):
        screen.blit(self.image, self.rect, self.subRect)
