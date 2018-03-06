# -*- coding: utf-8 -*-

from src.scenes.State import *

class InRoomState(State):

    def update(self, time, stage):
        # Actualizamos los sprites
        stage.spritesGroup.update(stage.rooms[stage.currentRoom].mask, time)

        # Alinea el viewport con el centro del jugador
        # Si la pantalla se sale de la sala actual, la alinea para que encaje
        # De este modo, el personaje siempre estará centrado, menos cuando se aproxime
        # a los bordes de la sala
        stage.viewport.center = stage.player.rect.center
        stage.viewport.clamp_ip(stage.rooms[stage.currentRoom].rect)

    def draw(self, screen, stage):
        # Muestro un color de fondo
        screen.fill((100, 200, 255))
        room = stage.rooms[stage.currentRoom]

        # Luego los Sprites sobre una copia del mapa de la sala
        newRoom = room.image.copy()
        stage.spritesGroup.draw(newRoom)

        # Se pinta la porción de la sala que coincide con el viewport
        screen.blit(newRoom, (0,0), stage.viewport)

    def events(self, events, stage):
        stage.player.move()
