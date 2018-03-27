# -*- coding: utf-8 -*-

import pygame, os, random
from src.ResourceManager import *
from src.sprites.characters.Enemy import *
from src.sprites.Trigger import *
from src.sprites.drops.Life import *
from src.sprites.drops.Soul import *
from src.sprites.Door import *
from src.sprites.doors.UnlockedDoor import *

# -------------------------------------------------
# Clase Room

class Room(object):
    def __init__(self, stageNum, roomNum, stage):
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
                if "drop" in enemy:
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

        # Cargamos la lista de puertas cerradas de la sala si existen
        self.lockedDoors = []
        if "lockedDoors" in data:
            for lockedDoor in data["lockedDoors"]:
                door = Door(lockedDoor["position"], lockedDoor["doorSprite"], stage.mask)
                self.lockedDoors.append(door)

        self.lockedDoorsGroup = pygame.sprite.Group(self.lockedDoors)

        # Cargamos la lista de puertas abiertas de la sala si existen
        unlockedDoors = []
        if "unlockedDoors" in data:
            for unlockedDoor in data["unlockedDoors"]:
                rect = pygame.Rect(unlockedDoor["collision"][0], unlockedDoor["collision"][1], unlockedDoor["collision"][2], unlockedDoor["collision"][3])
                wait = False
                if "wait" in unlockedDoor:
                    wait = unlockedDoor["wait"]
                door = UnlockedDoor(unlockedDoor["position"], unlockedDoor["doorSprite"], stage.mask, rect, wait)
                unlockedDoors.append(door)

        self.unlockedDoorsGroup = pygame.sprite.Group(unlockedDoors)

        # Cargamos la lista de triggers de la sala si existen
        triggersList = []
        if "triggers" in data:
            for triggerData in data["triggers"]:
                (x, y) = (triggerData["position"][0], triggerData["position"][1])
                width = triggerData["width"]
                height = triggerData["height"]
                door = None

                if "opens" in triggerData:
                    roomNum = triggerData["opens"][0]
                    doorNum  = triggerData["opens"][1]
                    door = stage.rooms[roomNum].lockedDoors[doorNum]

                trigger = Trigger(pygame.Rect((x, y), (width, height)), triggerData["dialogueFile"], door)
                trigger.change_position((x, y))
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
