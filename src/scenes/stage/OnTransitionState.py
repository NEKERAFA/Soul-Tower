# -*- coding: utf-8 -*-

import pygame
from src.scenes.Scene import *
from src.scenes.Stage import *
from src.scenes.stage.State import *

# -------------------------------------------------
# Clase OnTransitionState

class OnTransitionState(State):
    def __init__(self, connection, player):
        self.connection = connection
        self.scrollX = SCREEN_WIDTH
        self.scrollY = SCREEN_HEIGHT
        self.scrollPlayerX = player.rect.width+24
        self.scrollPlayerY = player.rect.height+24
        self.speed = 0.5
        self.speedPlayer = self.speed*3/5

    def update(self, time, stage):
        if self.connection["direction"] == "left" or self.connection["direction"] == "right":
            shiftX = int(self.speed*time)
            shiftPlayerX = int(self.speedPlayer*time)

            self.scrollX -= shiftX

            # Desplazamos el viewport en función de la dirección
            if self.connection["direction"] == "right":
                stage.viewport = stage.viewport.move(shiftX, 0)
            else:
                stage.viewport = stage.viewport.move(-shiftX, 0)

            # Desplazamos el jugador para que quede en la entrada de la nueva sala
            self.scrollPlayerX -= shiftPlayerX
            if self.scrollPlayerX > 0:
                if self.connection["direction"] == "right":
                    stage.player.increment_position((shiftPlayerX, 0))
                else:
                    stage.player.increment_position((-shiftPlayerX, 0))

            # Si hemos terminado de desplazar el mapa, volvemos al estado InRoomState y cambiamos la sala actual
            if self.scrollX <= 0:
                dstRoom = self.connection["to"]
                if stage.rooms[dstRoom].small:
                    stage.state = stage.smallRoomState
                else:
                    stage.state = stage.inRoomState
                stage.spritesGroup.remove(stage.rooms[stage.currentRoom].enemies.sprites())
                stage.currentRoom = dstRoom

        else:
            shiftY = int(self.speed*time)
            shiftPlayerY = int(self.speedPlayer*time)

            self.scrollY -= shiftY

            # Desplazamos el viewport en función de la dirección
            if self.connection["direction"] == "down":
                stage.viewport = stage.viewport.move(0, shiftY)
            else:
                stage.viewport = stage.viewport.move(0, -shiftY)

            # Desplazamos el jugador para que quede en la entrada de la nueva sala
            self.scrollPlayerY -= shiftPlayerY
            if self.scrollPlayerY > 0:
                if self.connection["direction"] == "down":
                    stage.player.increment_position((0, shiftPlayerY))
                else:
                    stage.player.increment_position((0, -shiftPlayerY))

            # Si hemos terminado de desplazar el mapa, volvemos al estado InRoomState y cambiamos la sala actual
            if self.scrollY <= 0:
                dstRoom = self.connection["to"]
                if stage.rooms[dstRoom].small:
                    stage.state = stage.smallRoomState
                else:
                    stage.state = stage.inRoomState
                stage.spritesGroup.remove(stage.rooms[stage.currentRoom].enemies.sprites())
                stage.currentRoom = dstRoom

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
