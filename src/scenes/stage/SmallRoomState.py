# -*- coding: utf-8 -*-

from src.controls.KeyboardMouseControl import *
from src.scenes.stage.StageState import *
from src.scenes.stage.OnLeaveState import *
from src.scenes.stage.OnTransitionState import *
from src.scenes.stage.OnDialogueState import *
from src.sprites.characters.Enemy import *
from src.sprites.drops.Life import *
from src.sprites.drops.Soul import *

class SmallRoomState(StageState):
    def update(self, time, stage):
        # Actualizamos los sprites
        # Player
        stage.player.update(time, stage)

        # Comprobamos si estamos saliendo de la sala
        exit = currentRoom.isExiting(stage.player)

        if exit is not None:
            if "next" in exit:
                stage.set_state(OnLeaveState())
            else:
                stage.set_state(OnTransitionState(exit, stage.player))
            return

        # Si detecta colisión con un trigger, cambia de estado
        trigger = pygame.sprite.spritecollideany(stage.player, currentRoom.triggers)

        if trigger is not None:
            trigger.open_door(stage)
            stage.state = OnDialogueState(trigger.dialogueFile, stage)
            trigger.kill() # Eliminamos el trigger
            return

        # Se detecta si estás en colisión con una puerta desbloqueada y si se
        # puede abrir
        for unlockedDoor in iter(currentRoom.unlockedDoorsGroup):
            # Colisión entre jugador y puerta
            if unlockedDoor.collision.colliderect(stage.player.rect) and KeyboardMouseControl.sec_button():
                unlockedDoor.open(stage)

    def events(self, events, stage):
        stage.player.move(stage.viewport)
