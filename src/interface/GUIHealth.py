# -*- encoding: utf-8 -*-

import pygame
from src.ResourceManager import *
from src.interface.GUIElement import *
from src.interface.GUIImage import *

# -------------------------------------------------
# Clase GUIHealth

class GUIHealth(GUIElement):
    def __init__(self, guiScreen, name, position, scale, lifeCounter, colorkey=-1):

        # String de la imagen del corazón
        self.name = name
        
        self.scale = scale
        self.colorkey = colorkey

        # Array de corazones a dibujar
        self.heartArray = []

        # Posicion de los corazones
        self.heartPos = position
        heart = None

        # Se llama al método de la clase padre con un rectángulo arbitrario (ya que este objeto no tiene imagen propia)
        GUIElement.__init__(self, guiScreen, pygame.Rect((0,0),(0,0)))
        # Se coloca el rectangulo en su posicion
        self.set_position(position)

        for i in range(0, lifeCounter):
            self.gain_life()

    def update(self, time):
        # Actualizar corazones
        for i in range(0, len(self.heartArray)):
            self.heartArray[i].update(time)
        return

    def draw(self, screen):
        # Dibujar corazones
        for i in range(0, len(self.heartArray)):
            self.heartArray[i].draw(screen)
        return

    def action(self):
        # Implementar animación de perder vida ?
        return

    def gain_life(self):
        # Crear corazón y meterlo en array
        heart = GUIImage(self.guiScreen, self.name, self.heartPos, self.scale, self.colorkey)
        self.heartArray.append(heart)
        # Actualizar posiciones del resto de corazones
        self.heartPos = (self.heartPos[0] + heart.image.get_rect().right, self.heartPos[1])

    def lose_life(self):
        # Eliminar último elemento del array
        if(len(self.heartArray) > 0):
            del(self.heartArray[-1])
