# -*- coding: utf-8 -*-

import pygame, os, random
from src.ResourceManager import *
from src.sprites.characters.Enemy import *
from src.sprites.drops.Life import *
from src.sprites.drops.Soul import *

# -------------------------------------------------
# Clase Room

class Room(object):
    def __init__(self, stageNum, roomNum):
        # Obtenemos el nombre de la sala
        fullname = os.path.join('stage_' + str(int(stageNum)), 'room_' + str(int(roomNum)) + '.json')

        # Llamamos al ResourceManager para cargar la sala
        data = ResourceManager.load_room(fullname)

        # Cargamos los datos del mapa
        self.position = (data["position"][0], data["position"][1])
        self.width = data["width"]
        self.height = data["height"]
        self.connections = data["connections"]
        self.rect = pygame.Rect(self.position, (self.width, self.height))
        self.small = True if "small" in data else False

        # Cargamos los enemigos de la sala si existien
        enemies = []
        if "enemies" in data:
            for enemy in data["enemies"]:
                # Load drop
                drop = None
                if enemy["drop"]["type"] == "life":
                    drop = Life(enemy["drop"]["amount"])
                elif enemy["drop"]["type"] == "soul":
                    drop = Soul(enemy["drop"]["amount"])

                # Load sprite
                enemySprite = Enemy(enemy["type"], drop)

                # Load position
                posX = random.randint(self.position[0]+24, self.position[0]+self.width-48)
                posY = random.randint(self.position[1]+24, self.position[1]+self.height-48)
                if "position" in enemy:
                    posX = enemy["position"][0]
                    posY = enemy["position"][1]
                enemySprite.change_global_position((posX, posY))
                enemies.append(enemySprite)
        self.enemies = pygame.sprite.Group(enemies)
        self.drops = pygame.sprite.Group()

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
