# -*- encoding: utf-8 -*-

import pygame
from math import floor, ceil
from src.ResourceManager import *
from src.interface.GUIImage import *

# TODO veremos si sigue haciendo falta
import os

# -------------------------------------------------
# Clase GUIDialog

class GUIDialog(GUIImage):
    def __init__(self, gui_screen, name, position, scale, font, text, textSpeed=0.02):
        GUIImage.__init__(self, gui_screen, name, position, scale)
        pygame.font.init()

        # Posición de inicio del texto
        self.textPositionX=self.rect.left+20
        self.textPositionY=self.rect.top+35
        # Texto a escribir
        self.fullText = text # TODO yyy local también creo
        self.maxSize = len(self.fullText) # TODO creo que también se puede hacer local
        # Fuente del texto
        self.font = font

        # Variables de control de la impresión
        self.printText = ""
        self.textCounter = 0 # TODO creo que se puede hacer local
        self.textSpeed = textSpeed
        self.nextLetter = 0 # TODO ya no haría falta
        # TODO meter un atributo tipo json que almacene el texto
        # TODO mostrar imagen del personaje
        # TODO mostrar nombre del personaje

        # TODO imagen de personaje
        path = os.path.join('interface', 'game', 'leraila.png')
        self.portrait = ResourceManager.load_image(path, -1)
        self.portrait_rect = self.portrait.get_rect()
        self.portrait_pos = (self.rect.right -self.portrait_rect.width-5, self.rect.bottom -5)
        self.portrait_rect.left = self.portrait_pos[0]
        self.portrait_rect.bottom = self.portrait_pos[1]

    def update(self, time):

        # if(self.textCounter<self.maxSize): #si el contador es menor que el tamaño del texto
        #     if(self.nextLetter==floor(self.textCounter)): #y es igual a la siguiente letra a escribir
        #         self.printText += self.fullText[self.nextLetter] #añadimos la siguiente letra a escribir en el texto que se imprime
        #         self.nextLetter+=1 #pasamos a la siguiente letra
        #     self.textCounter+=self.textSpeed*time #aumentamos, poco a poco (dependiendo del tiempo y la velocidad de escritura), el contador

        # Si queda texto por imprimir, calculamos cuántas letras debemos mostrar (en base al tiempo y la velocidad)
        # las mostramos e incrementamos el contador
        if (self.textCounter < self.maxSize):
            letters = int(ceil(self.textSpeed * time)) # Redondeamos hacia arriba para garantizar al menos una letra por frame
            limit = min(self.maxSize, self.textCounter + letters) # Nos aseguramos de no pasarnos de los límites del index
            self.printText += self.fullText[self.textCounter:(self.textCounter + letters)] # Añadimos las próximas letras a escribir
            self.textCounter += letters


    def draw(self, screen):
        # Crear surface con el texto
        textSurface = self.font.render(self.printText, False, (0,0,0))

        # Dibujar la imagen de fondo del diálogo (la caja)
        screen.blit(self.image, self.rect)
        # Dibujar el texto
        screen.blit(textSurface, (self.textPositionX, self.textPositionY))
        # TODO dibujar el retrato
        screen.blit(self.portrait, self.portrait_rect)

    def action(self):
        # No hace nada (es una imagen)
        return
