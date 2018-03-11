# -*- coding: utf-8 -*-

from src.scenes.State import *
from src.scenes.OnTransitionState import *

class InRoomState(State):

    def update(self, time, stage):
        # Actualizamos los sprites
        stage.spritesGroup.update(stage.mask, time)

        (playerX, playerY) = stage.player.rect.center

        # Comprobamos si estamos saliendo de la sala
        exit = stage.rooms[stage.currentRoom].isExiting(stage.player)

        if exit is not None:
            stage.state = OnTransitionState(exit, stage.player)
            return

        # Alinea el viewport con el centro del jugador
        # Si la pantalla se sale de la sala actual, la alinea para que encaje
        # De este modo, el personaje siempre estará centrado, menos cuando se aproxime
        # a los bordes de la sala
        stage.viewport.center = (stage.player.rect.center)
        stage.viewport.clamp_ip(stage.rooms[stage.currentRoom].rect)

    def draw(self, screen, stage):
        # Muestro un color de fondo
        screen.fill((100, 200, 255))
        # Luego los Sprites sobre una copia del mapa de la sala
        newImage = stage.image.copy()
        stage.spritesGroup.draw(newImage)
        # Se pinta la porción de la sala que coincide con el viewport
        screen.blit(newImage, (0,0), stage.viewport)

    def events(self, events, stage):
        stage.player.move(stage.viewport)
