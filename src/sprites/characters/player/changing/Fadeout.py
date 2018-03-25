# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
# Clase padre para controlar el cambio de estado

from src.sprites.characters.player.changing.ChangingState import *
from src.sprites.characters.player.changing.Finish import *

# Tiempo de la animación en milisegundos
MAX_TIME = 250.0

class Fadeout(ChangingState):
    def __init__(self):
        self.width = 0

    def update(self, player, time, stage):
        # Obtenemos el frame actual
        maxWidth = player.sheetConf[0][0]['coords'].width

        # Si el tamaño de la imagen ha llegado a 0 se cambia a la siguiente
        if self.width == maxWidth:
            # Cambiamos de estado
            player.changing = Finish()
        else:
            # Vamos aumentando poco a poco el tamaño del sprite
            # Calculamos el incremento
            increment = maxWidth / MAX_TIME
            # Calculamos el nuevo tamaño
            self.width = min(self.width+increment*time, maxWidth)
            # Obtenemos el alto de la imagen original
            height = player.origImage.get_height()
            # Escalamos la imagen original
            player.image = pygame.transform.scale(player.origImage, (int(self.width), height))
            # Centramos el rectángulo y lo escalamos
            center = player.rect.center
            player.rect.width = int(self.width)
            player.rect.center = center
