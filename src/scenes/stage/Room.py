# -*- coding: utf-8 -*-

import pygame, os, random
from src.ResourceManager import *
from src.sprites.characters.Enemy import *
from src.sprites.characters.Boss import *
from src.sprites.Trigger import *
from src.sprites.Drop import *
from src.sprites.Key import *
from src.sprites.Door import *
from src.sprites.doors.UnlockedDoor import *
from src.sprites.MagicWindow import *

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
        self.enemies = pygame.sprite.Group()
        if "enemies" in data:
            for enemy in data["enemies"]:
                # Cargamos el drop
                drop = Drop(enemy["drop"]["type"], enemy["drop"]["amount"])
                # Cargamos el sprite
                enemySprite = Enemy(enemy["type"], drop)
                # Ponemos al enemigo en su posición
                if "position" in enemy:
                    enemySprite.change_global_position(enemy["position"])
                else:
                    # Posición random
                    posX = random.randint(self.position[0]+24, self.position[0]+self.width-48)
                    posY = random.randint(self.position[1]+24, self.position[1]+self.height-48)
                    enemySprite.change_global_position((posX, posY))
                    offset = enemySprite.rect.topleft

                    # Comprobamos que no colisiona con la máscara
                    while enemySprite.mask.overlap(stage.mask, offset):
                        posX = random.randint(self.position[0]+24, self.position[0]+self.width-48)
                        posY = random.randint(self.position[1]+24, self.position[1]+self.height-48)
                        enemySprite.change_global_position((posX, posY))
                        offset = enemySprite.rect.topleft

                # Añadimos al enemigo en los sprites
                self.enemies.add(enemySprite)

        # Si hay un boss en la sala, lo cargo
        if "boss" in data:
            boss = data["boss"]
            drops = []
            for drop in boss["drops"]:
                drops.append(Drop(drop["type"], drop["amount"]))
            deathAnimation = None
            if "deathAnimation" in boss:
                deathAnimation = boss["deathAnimation"]
            bossSprite = Boss(boss["name"], drops, boss["closeDoor"], boss["finalDialogue"], deathAnimation)
            bossSprite.change_global_position(boss["position"])
            self.boss = bossSprite
            self.enemies.add(bossSprite)

        # Cargamos la lista de puertas cerradas de la sala si existen
        self.lockedDoors = []
        if "lockedDoors" in data:
            for lockedDoor in data["lockedDoors"]:
                door = Door(lockedDoor["position"], lockedDoor["doorSprite"], lockedDoor["doorMask"], stage)
                self.lockedDoors.append(door)
        self.doors = pygame.sprite.Group(self.lockedDoors)

        # Cargamos los objetos recolectables
        self.collectables = pygame.sprite.Group()
        self.keys = []
        if "keys" in data:
            for key in data["keys"]:
                keyObj = Key(key["position"], key["keySprite"])
                self.collectables.add(keyObj)
                self.keys.append(keyObj)

        # Cargamos los objetos con los que se pueda interactuar
        self.interactives = pygame.sprite.Group()

        # Cargamos la lista de puertas abiertas de la sala si existen
        self.unlockedDoors = []
        self.unlockedDoorsGroup = pygame.sprite.Group()
        if "unlockedDoors" in data:
            for unlockedDoor in data["unlockedDoors"]:
                rect = pygame.Rect(unlockedDoor["collision"][0], unlockedDoor["collision"][1], unlockedDoor["collision"][2], unlockedDoor["collision"][3])
                key = None
                if "key" in unlockedDoor:
                    key = unlockedDoor["key"]
                door = UnlockedDoor(unlockedDoor["position"], unlockedDoor["doorSprite"], unlockedDoor["doorMask"], stage, rect, key)
                self.unlockedDoors.append(door)
                self.unlockedDoorsGroup.add(door)
                self.interactives.add(door)

        # Cargamos la ventana mágica si existera
        self.magicWindowGroup = pygame.sprite.Group()
        if "magicWindow" in data:
            windowData = data["magicWindow"]
            magicWindow = MagicWindow(windowData["position"], windowData["initialDialog"], windowData["selectionFile"], windowData["endDialog"], windowData["collision"])
            self.magicWindowGroup.add(magicWindow)
            self.interactives.add(magicWindow)

        # Cargamos la lista de triggers de la sala si existen
        self.triggers = pygame.sprite.Group()
        if "triggers" in data:
            for triggerData in data["triggers"]:
                (x, y) = (triggerData["position"][0], triggerData["position"][1])
                width = triggerData["width"]
                height = triggerData["height"]
                door = None

                if "opens" in triggerData:
                    otherRoomNum = triggerData["opens"][0]
                    doorNum  = triggerData["opens"][1]
                    door = stage.rooms[otherRoomNum].lockedDoors[doorNum] if otherRoomNum != roomNum else self.lockedDoors[doorNum]

                trigger = Trigger(pygame.Rect((x, y), (width, height)), triggerData["dialogueFile"], door)
                trigger.change_position((x, y))
                self.triggers.add(trigger)

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
