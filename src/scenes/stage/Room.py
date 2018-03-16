# -*- coding: utf-8 -*-

import pygame, os, random
from src.ResourceManager import *
from src.sprites.characters.Enemy import *
from src.sprites.Trigger import *

# -------------------------------------------------
# Clase Room

class Room(object):
    def __init__(self, stageNum, roomNum):
        # Obtenemos el nombre de la sala
        fullname = os.path.join('stage_' + str(int(stageNum)), 'room_' + str(int(roomNum)) + '.json')

        # Llamamos al ResourceManager para cargar la sala
        data = ResourceManager.load_room(fullname)

        # Cargamos los datos del mapa
        self.position = (data["x"], data["y"])
        self.width = data["width"]
        self.height = data["height"]
        self.connections = data["connections"]
        self.rect = pygame.Rect(self.position, (self.width, self.height))
        self.small = True if "small" in data else False

        # Cargamos los enemigos de la sala si existien
        enemiesList = []
        if "enemies" in data:
            for enemy in data["enemies"]:
                # Load sprite
                enemySprite = Enemy(enemy["type"])
                # Load position
                posX = random.randint(self.position[0]+24, self.position[0]+self.width-48)
                posY = random.randint(self.position[1]+24, self.position[1]+self.height-48)
                if "position" in enemy:
                    posX = enemy["position"][0]
                    posY = enemy["position"][1]
                enemySprite.change_global_position((posX, posY))
                enemiesList.append(enemySprite)
        self.enemies = pygame.sprite.Group(enemiesList)

        # TODO Cargamos la lista de triggers de la sala si existen
        triggersList = []
        if "triggers" in data:
            for triggerData in data["triggers"]:
                (x, y) = (triggerData["position"][0], triggerData["position"][1])
                width = triggerData["width"]
                height = triggerData["height"]

                trigger = Trigger(pygame.Rect((x, y), (width, height)), triggerData["dialogueFile"])
                trigger.change_global_position((x, y))
                triggersList.append(trigger)

        self.triggers = pygame.sprite.Group(triggersList)


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