# -*- coding: utf-8 -*-

import pygame, string
from src.ResourceManager import *
from src.scenes.Scene import *
from src.scenes.screens.Room import *
from src.sprites.Player import *

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

        # Cargamos el sprite del jugador
        self.player = Player()
        self.player.change_global_position((100, 100))
        self.spritesGroup = pygame.sprite.Group(self.player)

    def update(self, time):
        # Actualizamos los sprites
        self.spritesGroup.update(self.rooms[self.currentRoom], time)

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
        # Imprimo la escena
        screen.blit(room.image, (room.x-self.scroll[0], room.y-self.scroll[1]))
        # Luego los Sprites
        self.spritesGroup.draw(screen)

	def actualizarScroll(self, player):
		changeScroll = False

		# Si el personaje se ha movido hacia la izquierda
		if (player.movement == W) or (player.movement == NW) or (player.movement == SW):
	        # Si el escenario ya está a la izquierda del todo, no lo movemos más, pero actualizamos el
	        if self.scroll[0] - int(SCREEN_WIDTH / 2) <= self.rooms[currentRoom].x:
	            self.scroll[0] = (player.position[0] + player.offset[0]) - self.rooms[currentRoom].x # El scroll en x se corresponde con la coordenada x del centro del personaje

	        # Si se puede hacer scroll a la izquierda
	        else:
	            self.scroll[0] = (player.position[0] + player.offset[0]) - self.rooms[currentRoom].x
	            changeScroll = True

		# Si el personaje se ha movido hacia la derecha
		if (player.movement == E) or (player.movement == NE) or (player.movement == SE):
	        # Si el escenario ya está a la derecha del todo, no lo movemos más
	        if self.scroll[0] + int(SCREEN_WIDTH / 2) >= self.rooms[currentRoom].x + self.rooms[currentRoom].width:
	            self.scroll[0] = (player.position[0] + player.offset[0]) - self.rooms[currentRoom].x

            # Si se puede hacer scroll a la derecha
            else:
				self.scroll[0] = (player.position[0] + player.offset[0]) - self.rooms[currentRoom].x
				changeScroll = True

        # Si se cambió el scroll, se desplazan todos los Sprites y el decorado
        if changeScroll:
            # Actualizamos la posición en pantalla de todos los Sprites según el scroll actual
            for sprite in iter(self.spritesGroup):
                sprite.change_screen_position(self.scroll)

            # Además, actualizamos la sala para que se muestre una parte distinta
            self.rooms[currentRoom].update(self.scroll)
