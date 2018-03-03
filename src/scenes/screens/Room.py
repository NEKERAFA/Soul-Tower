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

        # Llamamos al ResourceManager para cargar la mascara del mapa
        self.mask = ResourceManager.load_image(mask_file, (255, 0, 255))
        self.mask = pygame.mask.from_surface(self.mask, 127)

        # Llamamos al ResourceManager para cargar el mapa
        data = ResourceManager.load_room(room_file)
        self.rect.left = data["x"]
        self.y = data["y"]
        self.width = data["width"]
        self.height = data["height"]
        self.connections = data["connections"]
