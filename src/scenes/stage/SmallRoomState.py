# -*- coding: utf-8 -*-

from src.scenes.stage.State import *
from src.scenes.stage.OnTransitionState import *
from src.sprites.characters.Enemy import *

class SmallRoomState(State):
    def update(self, time, stage):
        currentRoom = stage.rooms[stage.currentRoom]

        # Movemos los enemigos
        for enemy in iter(currentRoom.enemies):
            enemy.move_ai(stage.player)

        # Actualizamos los sprites
        # Player
        stage.player.update(time, currentRoom.rect, stage.mask)
        # Enemigos
        currentRoom.enemies.update(time, currentRoom.rect, stage.mask)
        # Drops
        currentRoom.drops.update(time)

        # Comprobamos si estamos saliendo de la sala
        exit = currentRoom.isExiting(stage.player)

        if exit is not None:
            stage.state = OnTransitionState(exit, stage.player)
            return

        # TODO Detectar las colisiones con los triggerables (triggers y drops) y activar el que te devuelvan

    def draw(self, screen, stage):
        currentRoom = stage.rooms[stage.currentRoom]

        # Muestro un color de fondo
        screen.fill((100, 200, 255))
        # Luego los Sprites sobre una copia del mapa de la sala
        newImage = stage.image.copy()
        # Player
        newImage.blit(stage.player.image, stage.player.rect)
        # Enemigos
        currentRoom.enemies.draw(newImage)
        # Drops
        currentRoom.drops.draw(newImage)
        # Se pinta la porción de la sala que coincide con el viewport
        screen.blit(newImage, (0,0), stage.viewport)

    def events(self, events, stage):
        stage.player.move(stage.viewport)
