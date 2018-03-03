# -*- coding: utf-8 -*-

import pygame, string
from src.scenes.Scene import *
from src.ResourceManager import *
from src.scenes.screens.Room import *

# -------------------------------------------------
# Clase Stage

class Stage(Scene):
    def __init__(self, stageFile, gameManager):
        # Primero invocamos al constructor de la clase padre
        Scene.__init__(self, gameManager)
        # Cargamos la configuración del nivel
        data = ResourceManager.load_stage(stageFile)
        # Cargamos el scroll inicial
        self.scroll = (data["scroll"][0], data["scroll"][1])
        # Cargamos las rutas de las salas
        images = os.listdir("assets/images/rooms/" + data["path"])
        images.sort(key=string.lower)
        configs = os.listdir("assets/rooms/" + data["path"])
        configs.sort(key=string.lower)

        if len(configs)*2 != len(images):
            raise SystemExit, "Los archivos de imagenes y configuración no guardan relación"

        # Cargamos las salas
        pth_img = "rooms/" + data["path"] + "/"
        pth = data["path"] + "/"
        self.rooms = [Room(pth_img + images[i*2], pth_img + images[i*2+1], pth + configs[i]) for i in range(0, len(configs))]
        self.currentRoom = 0

    def update(self, time):
        pass

    def events(self, events):
        # Miramos a ver si hay algun evento de salir del programa
        for event in events:
            # Si se quiere salir, se le indica al director
            if event.type == pygame.QUIT:
                self.gameManager.program_exit()
                return

    def draw(self, screen):
        # Muestro un color de fondo
        screen.fill((100, 200, 255))
        room = self.rooms[self.currentRoom]
        # Imprimo la escena
        screen.blit(room.image, (room.x-self.scroll[0], room.y-self.scroll[1]))
