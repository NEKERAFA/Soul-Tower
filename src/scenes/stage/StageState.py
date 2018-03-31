# -*- coding: utf-8 -*-

import pygame
from src.controls.KeyboardMouseControl import *

class StageState(object):
    def update(self, time, stage):
        currentRoom = stage.rooms[stage.currentRoom]

        # Compruebo los enemigos muertos para coger su drop
        killedEnemies = []
        for enemy in iter(currentRoom.enemies):
            if enemy.killed:
                enemy.set_drop(currentRoom.collectables)
                killedEnemies.append(enemy)

        for enemy in killedEnemies:
            enemy.kill() # Quito los enemigos muertos

        # Se recorre la lista de recolectables colisionados
        collectables = pygame.sprite.spritecollide(stage.player, currentRoom.collectables, False)
        for collectable in collectables:
            collectable.collect(stage) # Los recojo

        # Se detecta si estás en colisión con un objeto con el que puedes
        # interactuar
        for interSprite in iter(currentRoom.interactives):
            # Colisión entre jugador y puerta
            if interSprite.collide(stage.player) and KeyboardMouseControl.action_button():
                interSprite.activate(stage)

    def draw(self, screen, stage):
        currentRoom = stage.rooms[stage.currentRoom]

        # Muestro un color de fondo
        screen.fill((0, 0, 0))
        # Luego los Sprites sobre una copia del mapa de la sala
        newImage = stage.image.copy()
        # Ventana mágica
        currentRoom.magicWindowGroup.draw(newImage)
        # Recolectables
        currentRoom.collectables.draw(newImage)
        # Enemigos
        for enemy in iter(currentRoom.enemies):
            enemy.draw(newImage)
        # currentRoom.enemies.draw(newImage)
        # Puertas
        currentRoom.doors.draw(newImage)
        # Sprites interactivos
        currentRoom.unlockedDoorsGroup.draw(newImage)
        # Player
        stage.player.draw(newImage)
        # Se pinta la porción de la sala que coincide con el viewport
        screen.blit(newImage, (0,0), stage.viewport)

    def events(self, events, stage):
        raise NotImplemented("Tiene que implementar el metodo events.")
