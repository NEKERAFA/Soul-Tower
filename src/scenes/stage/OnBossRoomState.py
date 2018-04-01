# -*- coding: utf-8 -*-

from src.controls.KeyboardMouseControl import *
from src.scenes.stage.StageState import *
from src.scenes.stage.OnLeaveState import *
from src.scenes.stage.OnDialogueState import *
from src.sprites.Character import *
from src.sprites.Door import *
from src.sprites.characters.Enemy import *

class OnBossRoomState(StageState):
    def __init__(self, stage):
        currentRoom = stage.rooms[stage.currentRoom]
        # Creamos la puerta que se cierra al entrar en la habitación
        doorConf = stage.rooms[stage.currentRoom].boss.closeDoor
        door = Door(doorConf["position"], doorConf["doorSprite"], doorConf["doorMask"], stage)
        # Añadimos el sprite
        currentRoom.lockedDoors.append(door)
        currentRoom.doors.add(door)
        # Para comprobar si el boss a muerto
        self.killedBoss = False
        # Para controlar la animación de entrada
        self.startAnimation = True

    def update(self, time, stage):
        currentRoom = stage.rooms[stage.currentRoom]
        boss = currentRoom.boss

        # Solo muevo al boss si no ha muerto ni está en una animación
        if not boss.killed and not boss.animationLoop:
            boss.move_ai(stage.player)

        # Actualizamos los sprites
        # Player
        stage.player.update(time, stage)
        # Boss
        boss.update(time, currentRoom.rect, stage)

        # Compruebo si el enemigo ha termina la animación
        if boss.animationFinish and self.startAnimation:
            boss.animationLoop = True
            boss.animationFinish = False
            boss.set_initial_frame(STILL)
            boss.change_behaviour(boss.initialState)
            self.startAnimation = False

        # Compruebo si ha muerto el boss para dropear
        if boss.killed and not self.killedBoss:
            boss.kill()
            boss.set_drop(currentRoom.collectables)
            currentRoom.lockedDoors[0].open(stage)
            self.killedBoss = True
            stage.set_state(OnDialogueState(boss.dialogueFile, stage))
            # Si hay una animación de muerte, lo deja quieto y lo muestra
            if boss.hasDeathAnimation:
                boss.movement = STILL
                boss.speed = (0, 0)
                boss.change_behaviour(boss.stillState)
                boss.animationLoop = False
                boss.set_initial_frame(boss.deathAnimation)
                self.deathAnimation = True

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

    def draw(self, screen, stage):
        currentRoom = stage.rooms[stage.currentRoom]

        # Muestro un color de fondo
        screen.fill((0, 0, 0))
        # Luego los Sprites sobre una copia del mapa de la sala
        newImage = stage.image.copy()
        # Boss
        currentRoom.boss.draw(newImage)
        # Recolectables
        currentRoom.collectables.draw(newImage)
        # Puertas
        currentRoom.doors.draw(newImage)
        # Sprites interactivos
        currentRoom.unlockedDoorsGroup.draw(newImage)
        # Player
        stage.player.draw(newImage)
        # Se pinta la porción de la sala que coincide con el viewport
        screen.blit(newImage, (0,0), stage.viewport)
