# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
# Clase padre para controlar el cambio de estado

from src.sprites.Character import *
from src.sprites.characters.player.changing.ChangingState import *
from src.sprites.characters.player.changing.Fadeout import *

class Fadein(ChangingState):
    def __init__(self, width):
        self.width = width

    def update(self, player, time, mapRect, mapMask):
        # Si el tamaño de la imagen ha llegado a 0 se cambia a la siguiente
        if self.width == 0:
            currentAnim = player.sheetConf[0]

            # Cambio de hechicera a guerrero
            if player.currentCharacter == 'sorcerer':
                player.currentCharacter = 'warrior'
                player.sheet = player.warriorSheet
            # Cambio de guerrero a hechicera
            elif player.currentCharacter == 'warrior':
                player.currentCharacter = 'sorcerer'
                player.sheet = player.sorcererSheet

            # Actualizamos el sprite con el nuevo sprite sheet
            player.origImage = player.sheet.subsurface(currentAnim[0]['coords'])

            # Cambiamos de estado
            player.changing = Fadeout()
        else:
            # Vamos disminuyendo poco a poco el tamaño del sprite
            self.width = max(self.width-2, 0)
            height = player.origImage.get_height()
            player.image = pygame.transform.scale(player.origImage, (self.width, height))
            center = player.rect.center
            player.rect.width = self.width
            player.rect.center = center
