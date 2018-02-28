# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
from pytmx import TiledImageLayer
from pytmx import TiledObjectGroup
from pytmx import TiledTileLayer
from src.ResourceManager import ResourceManager

# -------------------------------------------------
# Clase Room

class Room(object):
    def __init__(self, map_file, room_file):
        # Llamamos al ResourceManager para cargar el mapa
        self.data = ResourceManager.load_room(map_file, room_file)
        #print(repr(self.data))

    def events(self, list_events):
        pass

    def draw(self, screen):
        # Recorremos las capas visibles del mapa
        for layer in self.data["map"].visible_layers:
            # Si es una capa con información de tiles, se itera cada tile y se
            # muestra en pantalla
            if isinstance(layer, TiledTileLayer):
                for i, j, tile in layer.tiles():
                    screen.blit(tile, (i * self.data["map"].tilewidth, j * self.data["map"].tileheight))
