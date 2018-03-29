# -*- coding: utf-8 -*-

from src.controls.KeyboardMouseControl import *
from src.scenes.stage.StageState import *
from src.scenes.stage.OnLeaveState import *
from src.scenes.stage.OnDialogueState import *
from src.sprites.characters.behaviours.raven.RavenFlyAroundStageState import *
from src.sprites.characters.Enemy import *

class OnBossRoomState(StageState):
    def __init__(self, stage):
        stage.rooms[stage.currentRoom].boss.set_initial_frame(4)
        stage.rooms[stage.currentRoom].boss.animationLoop = False

    def update(self, time, stage):
        currentRoom = stage.rooms[stage.currentRoom]

        # Actualizamos los sprites
        # Player
        if currentRoom.boss.animationLoop:
            stage.player.update(time, stage)

        # Boss
        if not currentRoom.boss.killed:
            # Actualizamos el movimiento solo si la animación está en loop
            if currentRoom.boss.animationLoop:
                currentRoom.boss.move_ai(stage.player)

            # Actualiamos la animación
            currentRoom.boss.update(time, currentRoom.rect, stage.mask)

            # Compruebo si el enemigo ha termina la animación
            if currentRoom.boss.animationFinish:
                currentRoom.boss.animationLoop = True
                currentRoom.boss.animationFinish = False
                currentRoom.boss.set_initial_frame(0)
                currentRoom.boss.change_behaviour(RavenFlyAroundStageState())

        # Compruebo si ha muerto el boss
        if currentRoom.boss.killed and not stage.bossKilled:
            currentRoom.boss.kill()
            currentRoom.boss.set_drop(currentRoom.drops)
            stage.bossKilled = True

        # Drops
        currentRoom.drops.update(time)

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

        drops = pygame.sprite.spritecollide(stage.player, currentRoom.drops, False)

        # Se recorre la lista de drops colisionados
        for drop in drops:
            # Drops de vida
            if drop.name == 'heart':
                # Comprobamos que la vida del enemigo es menor que la máxima
                # (ha recibido daño)
                if stage.player.stats["hp"] < stage.player.stats["max_hp"]:
                    # Añadimos las vidas al jugador
                    stage.player.add_lifes(drop.amount)
                    # Eliminamos el sprite de todos los grupos
                    drop.kill()
            # Drops de almas
            elif drop.name == 'soul':
                # Añadimos las almas recogidas y eliminamos el sprite de todos
                # los grupos
                stage.player.increase_souls(drop.amount)
                drop.kill()

        # Se detecta si estás en colisión con un objeto con el que puedes
        # interactuar
        for interSprite in iter(currentRoom.interactivesGroup):
            # Colisión entre jugador y puerta
            if interSprite.collide(stage.player) and KeyboardMouseControl.sec_button():
                interSprite.activate(stage)

    def events(self, events, stage):
        stage.player.move(stage.viewport)
