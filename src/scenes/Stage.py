# -*- coding: utf-8 -*-

import pygame, string
from src.ResourceManager import *
from src.scenes.Scene import *
from src.scenes.screens.Room import *
from src.sprites.Player import *

# -------------------------------------------------
# Clase Stage

SCREEN_CENTER_X = int(SCREEN_WIDTH / 2)

class Stage(Scene):
    def __init__(self, stageFile, gameManager):
        # Primero invocamos al constructor de la clase padre
        Scene.__init__(self, gameManager)

        # Cargamos la configuración del nivel
        data = ResourceManager.load_stage(stageFile)

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

        # Cargamos el sprite del jugador
        self.player = Player()
        self.player.change_global_position((data["player_pos"][0], data["player_pos"][1]))
        self.spritesGroup = pygame.sprite.Group(self.player)

        # Calculamos el scroll inicial
        #self.scroll = ((self.player.position[0] + self.player.offset[0]) - self.rooms[self.currentRoom].x, (self.player.position[1] + self.player.offset[1]) - self.rooms[self.currentRoom].y)
        self.scroll = (0,0)

        # Inicializamos el viewport, que es un rectángulo del tamaño de la pantalla
        # que indicará qué porción de la sala se debe mostrar
        self.viewport = gameManager.screen.get_rect()
        self.viewport.center = self.player.rect.center
        self.viewport.clamp_ip(self.rooms[self.currentRoom].rect)

    def update(self, time):
        # Actualizamos los sprites
        self.spritesGroup.update(self.rooms[self.currentRoom].mask, time)

        # Actualizamos el scroll
        self.updateScroll()

    def events(self, events):
        # Miramos a ver si hay algun evento de salir del programa
        for event in events:
            # Si se quiere salir, se le indica al director
            if event.type == pygame.QUIT:
                self.gameManager.program_exit()
                return
        # Indicamos la acción a realizar para el jugador
        self.player.move()

    def draw(self, screen):
        # Muestro un color de fondo
        screen.fill((100, 200, 255))
        room = self.rooms[self.currentRoom]

        # Luego los Sprites sobre una copia del mapa de la sala
        newRoom = room.image.copy()
        self.spritesGroup.draw(newRoom)

        # Se pinta la porción de la sala que coincide con el viewport
        screen.blit(newRoom, (0,0), self.viewport)

    # Alinea el viewport con el centro del jugador
    # Si la pantalla se sale de la sala actual, la alinea para que encaje
    # De este modo, el personaje siempre estará centrado, menos cuando se aproxime
    # a los bordes de la sala
    def updateScroll(self):
        self.viewport.center = self.player.rect.center
        self.viewport.clamp_ip(self.rooms[self.currentRoom].rect)
