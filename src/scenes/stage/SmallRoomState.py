# -*- coding: utf-8 -*-

from src.scenes.stage.State import *
from src.scenes.stage.OnTransitionState import *
from src.scenes.stage.OnDialogueState import *

class SmallRoomState(State):

    def update(self, time, stage):
        # Actualizamos los sprites
        stage.spritesGroup.update(stage.rooms[stage.currentRoom].rect, stage.mask, time)

        (playerX, playerY) = stage.player.rect.center

        # Comprobamos si estamos saliendo de la sala
        exit = stage.rooms[stage.currentRoom].isExiting(stage.player)

        if exit is not None:
            stage.spritesGroup.add(stage.rooms[exit["to"]].enemies.sprites())
            stage.state = OnTransitionState(exit, stage.player)
            return

        # Si detecta colisión con un trigger, cambia de estado TODO cambiar a variable local currentRoom
        trigger = pygame.sprite.spritecollideany(stage.player, stage.rooms[stage.currentRoom].triggers)

        if trigger is not None:
            stage.state = OnDialogueState(trigger.dialogueFile, stage)
            trigger.kill() # Eliminamos el trigger
            return

    def events(self, events, stage):
        stage.player.move(stage.viewport)
