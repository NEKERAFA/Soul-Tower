# -*- encoding: utf-8 -*-

import pygame
from src.ResourceManager import *
from src.interface.GUIElement import *

# -------------------------------------------------
# Clase GUIButton

class GUIButton(GUIElement):
    def __init__(self, upName, downName, onClickFunction, position, scale=None, colorkey=-1):

        # Cargar las imágenes de botón sin pulsar y pulsado
        self.upImage = ResourceManager.load_image(upName, colorkey)
        self.downImage = ResourceManager.load_image(downName, colorkey)

        # Cambiar escala de las imágenes
        if scale is not None:
            self.upImage = pygame.transform.scale(self.upImage, scale)
            self.downImage = pygame.transform.scale(self.downImage, scale)

        # Variables para poder intercambiar las imágenes sin perder sus referencias
        self.activeImage = self.upImage
        self.inactiveImage = self.downImage

        # Función del botón
        self.onClickFunction = onClickFunction

        # Se llama al método de la clase padre con el rectángulo que ocupa el botón
        GUIElement.__init__(self, self.activeImage.get_rect())
        # Se coloca el rectangulo en su posicion
        self.set_position(position)

    def update(self, time):
        return

    def draw(self, screen):
        screen.blit(self.activeImage, self.rect)

    def swap(self):
        # Intercambiar imágenes
        temp = self.inactiveImage
        self.inactiveImage = self.activeImage
        self.activeImage = temp

    def action(self):
        # Intercambiar imágenes
        self.swap()
        # Si se ha pulsado y soltado el botón, activeImage será upImage, y se realiza la acción asociada
        if(self.activeImage == self.upImage):
            self.associated_action()

    def associated_action(self):
        # Acción asociada a cada botón
        self.onClickFunction()
