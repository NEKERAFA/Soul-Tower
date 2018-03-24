# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
# Clase padre para controlar el cambio de estado

from src.sprites.characters.player.changing.ChangingState import *
from src.sprites.characters.player.changing.Finish import *

class Fadeout(ChangingState):
    def __init__(self):
        self.width = 0

    def update(self, player, time, mapRect, mapMask):
        # Obtenemos el frame actual
        currentFrame = player.sheetConf[0][0]

        # Si el tamaño de la imagen ha llegado a 0 se cambia a la siguiente
        if self.width == currentFrame['coords'].width:
            # Cambiamos de estado
            player.changing = Finish()
        else:
            # Vamos aumentando poco a poco el tamaño del sprite
            self.width = min(self.width+2, currentFrame['coords'].width)
            height = player.origImage.get_height()
            player.image = pygame.transform.scale(player.origImage, (self.width, height))
            center = player.rect.center
            player.rect.width = self.width
            player.rect.center = center
