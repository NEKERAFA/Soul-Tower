# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
from src.ResourceManager import *
from src.screens.Screen import *

# -------------------------------------------------
# Clase Room

class Room(Screen):
    def __init__(self, map_file, mask_file, room_file):
        Screen.__init__(self, map_file)
        # Llamamos al ResourceManager para cargar la mascara del mapa
        self.mask = ResourceManager.load_image(mask_file, -1)
        self.mask = pygame.mask.from_surface(self.mask, 127)

        # Llamamos al ResourceManager para cargar el mapa
        data = ResourceManager.load_room(mask_file, room_file)
        self.x = data["x"]
        self.y = data["y"]
        self.width = data["width"]
        self.height = data["height"]
        self.connections = data["connections"]

    def draw(self, screen):
        Screen.draw(self, screen)

        # Esto lo hago para mostrar las paredes que no se pueden atravesar
        width, height = self.mask.get_size()
        tilemask = pygame.Surface((width, height))
        tilemask.set_alpha(128)
        for i in range(0, width):
            for j in range(0, height):
                if self.mask.get_at((i, j)) == 0:
                    tilemask.set_at((i, j), (0,0,0))
        screen.blit(tilemask, (self.x, self.y))
