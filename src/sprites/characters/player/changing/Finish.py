# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
# Esta clase controla que el cambio de personaje ha acabado y controla cuando
# empieza otro nuevo cambio de personaje

from src.sprites.Character import *
from src.sprites.characters.player.changing.ChangingState import *
from src.controls.KeyboardMouseControl import *

class Finish(ChangingState):
    def update(self, player, time, mapRect, mapMask):
        # Delegamos en el estado del jugador para actualizar
        player.state.update_pos(player, time, mapRect, mapMask)
        # Actualizamos el ataque
        player.attack.update(time)

        # Si se pulsa el botón de cambio de jugador
        if KeyboardMouseControl.select_button() and player.canChange:
            # Actualizamos la posición
            Character.move(player, STILL)
            player.update_animation(time)
            # Cambiamos de estado
            player.changing = Fadein(player.origImage.get_width())

from src.sprites.characters.player.changing.Fadein import *
