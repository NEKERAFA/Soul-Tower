# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
# Esta clase controla que el cambio de personaje ha acabado y controla cuando
# empieza otro nuevo cambio de personaje

from src.sprites.Character import *
from src.sprites.characters.player.changing.ChangingState import *
from src.controls.KeyboardMouseControl import *

class Finish(ChangingState):
    def update(self, player, time, stage):
        currentRoom = stage.rooms[stage.currentRoom]

        # Delegamos en el estado del jugador para actualizar
        player.state.update_state(player, time, currentRoom.rect, stage.mask)
        # Actualizamos el ataque
        player.attack.update(player, time, stage)

        # Si se pulsa el botón de cambio de jugador
        if KeyboardMouseControl.select_button() and player.canChange:
            # Ponemos la posición de parado
            Character.move(player, STILL)

            # Cogemos el rectángulo de vista frontal
            currentRect = player.sheetConf[0][0]['coords']
            # Actualizamos el sprite con el nuevo sprite sheet
            player.origImage = player.sheet.subsurface(currentRect)
            # Actualizamos el sprite que se dibuja
            player.image = player.origImage.copy()
            # Actualizamos el delay
            self.currentDelay = player.sheetConf[0][0]['delay']

            # Cambiamos de estado
            player.changing = Fadein(player.origImage.get_width())

from src.sprites.characters.player.changing.Fadein import *
