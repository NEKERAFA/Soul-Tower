# -*- encoding: utf-8 -*-

import pygame
from src.ResourceManager import *
from src.interface.GUIElement import *
from src.sprites.characters.player.changing.Fadein import *

SORCERESS_SYMBOL_SPRITE = 'interface/player/sorceress_symbol.png'
WARRIOR_SYMBOL_SPRITE = 'interface/player/warrior_symbol.png'
# -------------------------------------------------
# Clase GUICharacterSymbol
# Clase para mostrar un símbolo que represente al personaje activo

class GUICharacterSymbol(GUIElement):
    def __init__(self, guiScreen, position, scale, colorkey=-1):
        self.switching = False
        self.restoring = False
        # Una imagen para cada personaje
        self.sorcImage = ResourceManager.load_image(SORCERESS_SYMBOL_SPRITE, colorkey)
        self.warImage = ResourceManager.load_image(WARRIOR_SYMBOL_SPRITE, colorkey)
        # Cambiar escala
        if scale is not None:
            self.sorcImage = pygame.transform.scale(self.sorcImage, scale)
            self.warImage = pygame.transform.scale(self.warImage, scale)

        # Variables para poder intercambiar las imágenes
        self.activeImage = self.sorcImage
        self.inactiveImage = self.warImage

        self.drawnImage = self.activeImage

        # Se llama al método de la clase padre con el rectángulo que ocupa la imagen
        GUIElement.__init__(self, guiScreen, self.drawnImage.get_rect())
        # Se coloca el rectangulo en su posicion
        self.set_position(position)

        self.originalWidth = self.rect.width

        # Porcentaje de tamaño de la imagen; 1 -> la imagen se dibuja a tamaño normal
        self.percent = 1.
        # Velocidad de escalado de la imagen: 100% de la imagen/1000ms = 100% en 1s
        self.speed = self.originalWidth/MAX_TIME


    def update(self, time):
        if(self.switching):
            # Encoger imagen sobre su centro por el eje horizontal,
            #  para hacer un efecto de "moneda" girando
            if(self.rect.width > 0.):
                center = self.rect.center
                self.rect.width = int(max(0., self.rect.width-self.speed*time))
                scale = (self.rect.width, self.rect.height)
                self.drawnImage = pygame.transform.scale(self.activeImage, scale)
                self.rect.center = center
            else:
                # Intercambiar imágenes y pasar a la fase de expansión
                self.switching = False
                self.switch_image()
                self.restoring = True
        elif(self.restoring):
            # Expandir siguiente imagen para completar el efecto de la moneda
            if(self.rect.width < self.originalWidth):
                center = self.rect.center
                self.rect.width = int(min(self.originalWidth, self.rect.width+self.speed*time))
                scale = (self.rect.width, self.rect.height)
                self.drawnImage = pygame.transform.scale(self.activeImage, scale)
                self.rect.center = center
            else:
                self.restoring = False

        return

    def draw(self, screen):
        screen.blit(self.drawnImage, self.rect)

    def action(self):
        # Dar comienzo al intercambio de imágenes
        if(not self.switching and not self.restoring):
            self.switching = True

    def switch_image(self):
        # Intercambio de imágenes
        temp = self.inactiveImage
        self.inactiveImage = self.activeImage
        self.activeImage = temp
