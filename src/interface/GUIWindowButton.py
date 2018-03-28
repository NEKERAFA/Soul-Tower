# -*- encoding: utf-8 -*-

import pygame
from src.ResourceManager import *
from src.interface.GUIButton import *
from src.interface.GUIText import *

# -------------------------------------------------
# Clase GUIWindowButton
# Botones específicos de las ventanas mágicas, con un GUIText a mayores

# Fuentes
DEFAULT_FONT = 'PixelOperatorHB.ttf'
DEFAULT_FONT_SIZE = 16

class GUIWindowButton(GUIButton):
    def __init__(self, guiScreen, text, upName, downName, position, scale, onClickFunction, colorkey=-1):

        # Crear botón
        GUIButton.__init__(self, guiScreen, upName, downName, position, scale, onClickFunction, colorkey)

        # Crear texto
        self.font = ResourceManager.load_font(DEFAULT_FONT, DEFAULT_FONT_SIZE)
        self.textPosition = self.rect.center
        self.text = GUIText(self, self.textPosition, self.font, text, 'center', (255, 255, 255))

        self.swapHeight = 0

    def draw(self, screen):
        GUIButton.draw(self, screen)
        GUIText.draw(self.text, screen)

    def swap(self):
        # Intercambiar imágenes
        temp = self.inactiveImage
        self.inactiveImage = self.activeImage
        self.activeImage = temp

        # Mover texto arriba/abajo
        if(self.swapHeight == 4):
            self.swapHeight = 0
        else:
            self.swapHeight = 4
        self.text.set_position((self.rect.center[0], self.rect.center[1]+self.swapHeight))


    def action(self):
        # Intercambiar imágenes
        self.swap()

        # Si se ha pulsado y soltado el botón, activeImage será upImage, y se realiza la acción asociada
        if(self.activeImage == self.upImage):
            self.associated_action()
