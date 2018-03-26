# -*- coding: utf-8 -*-

from src.scenes.stage.StageState import *
from src.scenes.stage.OnTransitionState import *
from src.scenes.stage.OnDialogueState import *
from src.sprites.characters.Enemy import *

class SmallRoomState(StageState):
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

        # Si detecta colisión con un trigger, cambia de estado TODO cambiar a variable local currentRoom
        trigger = pygame.sprite.spritecollideany(stage.player, stage.rooms[stage.currentRoom].triggers)

        if trigger is not None:
            trigger.open_door()
            stage.state = OnDialogueState(trigger.dialogueFile, stage)
            trigger.kill() # Eliminamos el trigger
            return

    def events(self, events, stage):
        stage.player.move(stage.viewport)
