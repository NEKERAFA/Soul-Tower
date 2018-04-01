# -*- coding: utf-8 -*-

import pygame
from src.interface.GUIImage import *

# -------------------------------------------------
# Clase GUITutorialImage

class GUITutorialImage(GUIImage):
    def __init__(self, guiScreen, name, position, scale, associatedKey, colorkey=None):
        self.shrink = False
        # pygame.Key asociada
        self.associatedKey = associatedKey

        self.guiScreen = guiScreen
        GUIImage.__init__(self, name, position, scale, colorkey)

        # Porcentaje de tamaño de la imagen; 1 -> la imagen se dibuja a tamaño normal
        self.percent = 1
        # Velocidad de escalado de la imagen: 100% de la imagen/1000ms = 100% en 1s
        self.speed = 1./150.

        # Variables para controlar desaparición de la imagen
        self.originalImage = self.image
        self.originalWidth = self.rect.width
        self.originalHeight = self.rect.height

    def update(self, time):
        # Hacer desaparecer la imagen encogiéndola hacia su centro
        if(self.shrink):
            if(self.percent > 0.):
                center = self.rect.center
                self.percent = max(0., self.percent-time*self.speed)
                self.rect.width = int(self.originalWidth*self.percent)
                self.rect.height = int(self.originalHeight*self.percent)
                scale = (self.rect.width, self.rect.height)
                self.image = pygame.transform.scale(self.originalImage, scale)

                self.rect.center = center
            else:
                # Al terminar, eliminarse del array GUIElements
                self.guiScreen.remove_element(self)

    def action(self):
        self.shrink = True
