# -*- coding: utf-8 -*-

from src.controls.KeyboardMouseControl import *
from src.scenes.stage.StageState import *
from src.scenes.stage.OnLeaveState import *
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
        stage.player.update(time, stage)
        # Enemigos
        currentRoom.enemies.update(time, currentRoom.rect, stage)
        # Recogibles
        currentRoom.collectables.update(time)
        # Ventana mágica
        currentRoom.magicWindowGroup.update(time)

        # Si detecta colisión con un trigger, cambia de estado
        trigger = pygame.sprite.spritecollideany(stage.player, currentRoom.triggers)

        if trigger is not None:
            trigger.open_door(stage)
            stage.state = OnDialogueState(trigger.dialogueFile, stage)
            trigger.kill() # Eliminamos el trigger
            return

        # Comprobamos si estamos saliendo de la sala
        exit = currentRoom.isExiting(stage.player)

        if exit is not None:
            if "next" in exit:
                stage.set_state(OnLeaveState())
            else:
                stage.set_state(OnTransitionState(exit, stage.player))
            return

        StageState.update(self, time, stage)

        stage.gui.update(time)

    def events(self, events, stage):
        stage.player.move(stage.viewport)
        stage.gui.events(events)
