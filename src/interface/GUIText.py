# -*- encoding: utf-8 -*-

import pygame
from src.interface.GUIElement import *

# -------------------------------------------------
# Clase GUIText
# Clase para representar un texto de forma genérica, pudiendo cambiar
#  fuente, contenido, alineación o color

class GUIText(GUIElement):
    def __init__(self, guiScreen, position, font, text='', alignment='left', color=(0,0,0)):
        # Propiedades del texto
        self.font = font
        self.text = text
        self.color = color
        self.alignment = alignment

        self.textSurface = self.font.render(self.text, False, self.color)
        # Se llama al método de la clase padre con el rectángulo del texto
        GUIElement.__init__(self, guiScreen, self.textSurface.get_rect())
        # Se coloca el rectangulo en su posicion
        if(self.alignment=='left'):
            self.rect.bottomleft = position
        elif(self.alignment=='center'):
            self.rect.midbottom = position
        elif(self.alignment=='right'):
            self.rect.bottomright = position

    def update(self, time):
        return

    def draw(self, screen):
        screen.blit(self.textSurface, self.rect)

    def action(self):
        #No hace nada (es un texto)
        return

    def change_font(self, font):
        # Cambiar fuente del texto
        self.font = font
        self.update_text_surface()

    def change_text(self, str):
        # Cambiar texto
        self.text = str
        self.update_text_surface()

    def change_color(self, color):
        # Cambiar color del texto
        self.color = color
        self.update_text_surface()

    def change_alignment(self, alignment):
        # Cambiar alineación del texto
        self.alignment = alignment
        self.update_text_surface()

    def update_text_surface(self):
        # Cada vez que se haga un cambio se tiene que actualizar la Surface del texto
        self.textSurface = self.font.render(self.text, False, self.color)
        self.rect = self.textSurface.get_rect()
        # Se coloca el rectangulo en su posicion
        if(self.alignment=='left'):
            self.rect.bottomleft = position
        elif(self.alignment=='center'):
            self.rect.midbottom = position
        elif(self.alignment=='right'):
            self.rect.bottomright = position
