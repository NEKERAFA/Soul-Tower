# -*- coding: utf-8 -*-

class StageState(object):

    def __init__(self):
        pass

    def update(self, time, stage):
        raise NotImplemented("Tiene que implementar el metodo update.")

    def draw(self, screen, stage):
        currentRoom = stage.rooms[stage.currentRoom]

        # Muestro un color de fondo
        screen.fill((0, 0, 0))
        # Luego los Sprites sobre una copia del mapa de la sala
        newImage = stage.image.copy()
        # Puertas
        currentRoom.lockedDoorsGroup.draw(newImage)
        currentRoom.unlockedDoorsGroup.draw(newImage)
        # Player
        stage.player.draw(newImage)
        # Enemigos
        currentRoom.enemies.draw(newImage)
        # Drops
        currentRoom.drops.draw(newImage)
        # Se pinta la porción de la sala que coincide con el viewport
        screen.blit(newImage, (0,0), stage.viewport)

    def events(self, events, stage):
        raise NotImplemented("Tiene que implementar el metodo events.")
