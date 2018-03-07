# -*- coding: utf-8 -*-

import pygame
from src.ResourceManager import *

# -------------------------------------------------
# Clase Room

class Room(object):
    def __init__(self, roomFile):
        # Llamamos al ResourceManager para cargar la mascara del mapa
        # self.mask = ResourceManager.load_image(mask_file, -1)
        # self.mask = pygame.mask.from_surface(self.mask, 127)

        # Llamamos al ResourceManager para cargar el mapa
        data = ResourceManager.load_room(roomFile)
        self.position = (data["x"], data["y"])
        self.width = data["width"]
        self.height = data["height"]
        self.connections = data["connections"]
        self.rect = pygame.Rect(self.position, (self.width, self.height))
