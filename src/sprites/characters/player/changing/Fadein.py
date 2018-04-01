# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
# Clase padre para controlar el cambio de estado

from src.sprites.Character import *
from src.sprites.characters.player.changing.ChangingState import *
from src.sprites.characters.player.changing.Fadeout import *

# Tiempo de la animación en milisegundos
MAX_TIME = 250.0

class Fadein(ChangingState):
    def __init__(self, width, canChange):
        self.width = width
        self.canChange = canChange

    def update(self, player, time, stage):
        # Cogemos el rectángulo del frame de estar quieto
        currentRect = player.sheetConf[0][0]['coords']

        # Si el tamaño de la imagen ha llegado a 0 se cambia a la siguiente
        if self.width == 0:
            # Cambio de hechicera a guerrero
            if player.currentCharacter == 'sorcerer':
                player.currentCharacter = 'warrior'
                player.sheet = player.warriorSheet
            # Cambio de guerrero a hechicera
            elif player.currentCharacter == 'warrior':
                player.currentCharacter = 'sorcerer'
                player.sheet = player.sorcererSheet

            # Actualizamos el sprite con el nuevo sprite sheet
            player.origImage = player.sheet.subsurface(currentRect)

            # Cambiamos de estado
            player.changing = Fadeout(self.canChange)
        else:
            # Vamos disminuyendo poco a poco el tamaño del sprite
            # Calculamos el decremento
            decrement = player.origImage.get_width() / MAX_TIME
            # Calculamos el nuevo tamaño
            self.width = max(self.width-decrement*time, 0)
            # Obtenemos el alto de la imagen original
            height = player.origImage.get_height()
            # Escalamos la imagen original
            player.image = pygame.transform.scale(player.origImage, (int(self.width), height))
            # Centramos el rectángulo y lo escalamos
            center = player.rect.center
            player.rect.width = int(self.width)
            player.rect.center = center
