# -*- coding: utf-8 -*-

from src.controls.KeyboardMouseControl import *
from src.scenes.stage.StageState import *
from src.scenes.stage.OnLeaveState import *
from src.scenes.stage.OnDialogueState import *
from src.sprites.characters.Enemy import *
from src.sprites.Door import *

class OnBossRoomState(StageState):
    def __init__(self, stage):
        currentRoom = stage.rooms[stage.currentRoom]
        # Iniciamos la animación del boss
        currentRoom.boss.set_initial_frame(4)
        currentRoom.boss.animationLoop = False
        # Creamos la puerta que se cierra al entrar en la habitación
        doorConf = stage.rooms[stage.currentRoom].boss.closeDoor
        door = Door(doorConf["position"], doorConf["doorSprite"], doorConf["doorMask"], stage)
        # Añadimos el sprite
        currentRoom.lockedDoors.append(door)
        currentRoom.doors.add(door)
        # Para comprobar si el boss a muerto
        self.killedBoss = False

    def update(self, time, stage):
        currentRoom = stage.rooms[stage.currentRoom]

        # Actualizamos los sprites
        # Player
        stage.player.update(time, stage)

        # Boss
        if not currentRoom.boss.killed:
            # Actualizamos el movimiento solo si la animación está en loop
            if currentRoom.boss.animationLoop:
                currentRoom.boss.move_ai(stage.player)

            # Actualiamos la animación
            currentRoom.boss.update(time, currentRoom.rect, stage)

            # Compruebo si el enemigo ha termina la animación
            if currentRoom.boss.animationFinish:
                currentRoom.boss.animationLoop = True
                currentRoom.boss.animationFinish = False
                currentRoom.boss.set_initial_frame(0)
                currentRoom.boss.change_behaviour(currentRoom.boss.initialState)

        # Compruebo si ha muerto el boss para dropear el bo
        if currentRoom.boss.killed and not self.killedBoss:
            currentRoom.boss.kill()
            currentRoom.boss.set_drop(currentRoom.collectables)
            currentRoom.lockedDoors[0].open(stage)
            self.killedBoss = True
            if currentRoom.boss.dialogueFile != "":
                stage.set_state(OnDialogueState(currentRoom.boss.dialogueFile, stage))

        # Recogibles
        currentRoom.collectables.update(time)

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

        # Alinea el viewport con el centro del jugador
        # Si la pantalla se sale de la sala actual, la alinea para que encaje
        # De este modo, el personaje siempre estará centrado, menos cuando se aproxime
        # a los bordes de la sala
        stage.viewport.center = (stage.player.rect.center)
        stage.viewport.clamp_ip(currentRoom.rect)

        StageState.update(self, time, stage)

        # Actualizamos la interfaz
        stage.gui.update(time)

    def events(self, events, stage):
        stage.player.move(stage.viewport)

        # Actualizamos los eventos de la interfaz
        stage.gui.events(events)
