# -*- coding: utf-8 -*-

from src.scenes.stage.StageState import *
from src.scenes.stage.OnTransitionState import *
from src.scenes.stage.OnDialogueState import *
from src.sprites.characters.Enemy import *
from src.sprites.drops.Life import *
from src.sprites.drops.Soul import *

class InRoomState(StageState):
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

        # Alinea el viewport con el centro del jugador
        # Si la pantalla se sale de la sala actual, la alinea para que encaje
        # De este modo, el personaje siempre estará centrado, menos cuando se aproxime
        # a los bordes de la sala
        stage.viewport.center = (stage.player.rect.center)
        stage.viewport.clamp_ip(currentRoom.rect)

        # TODO Detectar las colisiones con los triggerables (triggers y drops) y activar el que te devuelvan

        drops = pygame.sprite.spritecollide(stage.player, currentRoom.drops, False)

        for drop in drops:
            if type(drop) is Life:
                # TODO max life y life
                print "More life:", drop.amount
            elif type(drop) is Soul:
                stage.player.increase_souls(drop.amount)
                drop.kill()

        # Si detecta colisión con un trigger, cambia de estado TODO cambiar a variable local currentRoom
        trigger = pygame.sprite.spritecollideany(stage.player, stage.rooms[stage.currentRoom].triggers)

        if trigger is not None:
            stage.state = OnDialogueState(trigger.dialogueFile, stage)
            trigger.kill() # Eliminamos el trigger
            return


    def events(self, events, stage):
        stage.player.move(stage.viewport)
