# -*- coding: utf-8 -*-

from src.controls.KeyboardMouseControl import *
from src.scenes.stage.StageState import *
from src.scenes.stage.OnLeaveState import *
from src.scenes.stage.OnTransitionState import *
from src.scenes.stage.OnDialogueState import *
from src.sprites.characters.Enemy import *

class InRoomState(StageState):
    def update(self, time, stage):
        currentRoom = stage.rooms[stage.currentRoom]

        # Movemos los enemigos
        for enemy in iter(currentRoom.enemies):
            enemy.move_ai(stage.player)

        # Actualizamos los sprites
        # Player
        stage.player.update(time, stage)
        # Enemigos
        currentRoom.enemies.update(time, currentRoom.rect, stage.mask)

        # Compruebo los enemigos muertos para matarlos y coger su drop
        killedEnemies = []
        for enemy in iter(currentRoom.enemies):
            if enemy.killed:
                enemy.set_drop(currentRoom.drops)
                killedEnemies.append(enemy)

        for enemy in killedEnemies:
            enemy.kill()

        # Drops
        currentRoom.drops.update(time)
        # Ventana mágica
        currentRoom.magicWindowGroup.update(time, stage)

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

        # Si detecta colisión con un trigger, cambia de estado
        trigger = pygame.sprite.spritecollideany(stage.player, currentRoom.triggers)

        if trigger is not None:
            trigger.open_door(stage)
            stage.state = OnDialogueState(trigger.dialogueFile, stage)
            trigger.kill() # Eliminamos el trigger
            return

        # Se detecta si estás en colisión con un objeto con el que puedes
        # interactuar
        for interSprite in iter(currentRoom.interactivesGroup):
            # Colisión entre jugador y puerta
            if interSprite.collide(stage.player) and KeyboardMouseControl.sec_button():
                interSprite.activate(stage)

        stage.gui.update(time)

    def events(self, events, stage):
        stage.player.move(stage.viewport)
        stage.gui.events(events)
