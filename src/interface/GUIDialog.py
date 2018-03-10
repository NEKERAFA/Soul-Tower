# -*- encoding: utf-8 -*-

import pygame
from math import floor
from src.ResourceManager import *
from src.interface.GUIImage import *

# -------------------------------------------------
# Clase GUIDialog

class GUIDialog(GUIImage):
    def __init__(self, gui_screen, name, position, scale, font, text, textSpeed=0.02):
        GUIImage.__init__(self, gui_screen, name, position, scale)
        pygame.font.init()

        # Posición de inicio del texto
        self.textPositionX=self.rect.left+20
        self.textPositionY=self.rect.top+50
        # Texto a escribir
        self.fullText = text
        self.maxSize = len(self.fullText)
        # Fuente del texto
        self.font = font

        # Variables de control de la impresión
        self.printText = ""
        self.textCounter = 0
        self.textSpeed = textSpeed
        self.nextLetter = 0

    def update(self, time):

        if(self.textCounter<self.maxSize): #si el contador es menor que el tamaño del texto
            if(self.nextLetter==floor(self.textCounter)): #y es igual a la siguiente letra a escribir
                self.printText += self.fullText[self.nextLetter] #añadimos la siguiente letra a escribir en el texto que se imprime
                self.nextLetter+=1 #pasamos a la siguiente letra
            self.textCounter+=self.textSpeed*time #aumentamos, poco a poco (dependiendo del tiempo y la velocidad de escritura), el contador

    def draw(self, screen):
        # Crear surface con el texto
        textSurface = self.font.render(self.printText, False, (0,0,0))

        # Dibujar la imagen de fondo del diálogo (la caja)
        screen.blit(self.image, self.rect)
        # Dibujar el texto
        screen.blit(textSurface, (self.textPositionX, self.textPositionY))

    def action(self):
        # No hace nada (es una imagen)
        return
