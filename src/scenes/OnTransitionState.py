# -*- coding: utf-8 -*-

import pygame
from src.scenes.State import *
from src.scenes.Scene import *
from src.scenes.Stage import *

# -------------------------------------------------
# Clase OnTransitionState

class OnTransitionState(State):
    def __init__(self, connection, playerWidth):
        self.connection = connection
        self.scrollX = SCREEN_WIDTH
        self.scrollPlayerX = playerWidth
        self.speedX = 0.5
        self.speedPlayerX = self.speedX*3/5

    def update(self, time, stage):
        print(self.scrollX, stage.viewport.center)

        shiftX = int(self.speedX*time)
        shiftPlayerX = int(self.speedPlayerX*time)

        self.scrollX -= shiftX
        stage.viewport = stage.viewport.move(shiftX, 0)
        self.scrollPlayerX -= shiftPlayerX

        if self.scrollPlayerX > 0:
            stage.player.increment_position((shiftPlayerX, 0))

        if self.scrollX <= 0:
            stage.state = stage.inRoomState
            stage.currentRoom = self.connection["to"]
            # stage.player.change_global_position((757, 247))

    def events(self, time, stage):
        pass

    def draw(self, screen, stage):
        # Muestro un color de fondo
        screen.fill((100, 200, 255))
        # Luego los Sprites sobre una copia del mapa de la sala
        newImage = stage.image.copy()
        stage.spritesGroup.draw(newImage)
        # Se pinta la porción de la sala que coincide con el viewport
        screen.blit(newImage, (0,0), stage.viewport)

        # room1 = stage.rooms[stage.currentRoom]
        # room2 = stage.rooms[self.connection["to"]]
        # room1Top = min(int(SCREEN_HEIGHT/2) - (stage.player.rect.centery - room1.position[1]), 0)
        # room2Top = min(int(SCREEN_HEIGHT/2) - (stage.player.rect.centery - room2.position[1]), 0)
        #
        # screen.blit(room1.image, pygame.Rect((self.scrollX-room1.width, room1Top), (self.scrollX, SCREEN_HEIGHT)))
        # screen.blit(room2.image, pygame.Rect((self.scrollX, room2Top), (SCREEN_WIDTH-self.scrollX, SCREEN_HEIGHT)))

        # Luego los Sprites sobre una copia del mapa de la sala
        #newRoom = room.image.copy()
        #stage.spritesGroup.draw(newRoom)

        # Se pinta la porción de la sala que coincide con el viewport
        #screen.blit(newRoom, (0,0), stage.viewport)
