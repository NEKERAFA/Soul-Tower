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
        self.small = True if "small" in data else False

    # Indica si el jugador está saliendo de la sala y devuelve la conexión que representa la salida
    def isExiting(self, player):
        (playerX, playerY) = player.rect.center
        exit = None
        for connection in self.connections:
            if (connection["direction"] == "right" and playerX > connection["x"]) or (connection["direction"] == "left" and playerX < connection["x"]):
                if playerY < connection["top"] and playerY > connection["bottom"]:
                    exit = connection
                    break
            elif (connection["direction"] == "up" and playerY < connection["y"]) or (connection["direction"] == "down" and playerY > connection["y"]):
                if playerX < connection["right"] and playerX > connection["left"]:
                    exit = connection
                    break

        return exit
