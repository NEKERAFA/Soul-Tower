# -*- encoding: utf-8 -*-

import pygame
from src.interface.GUIElement import *

# -------------------------------------------------
# Clase GUIImage

class GUIText(GUIElement):
    def __init__(self, guiScreen, position, font, text='', color=(0,0,0)):
        self.font = font
        self.text = text
        self.color = color
        self.update_text_surface()
        # Se llama al método de la clase padre con el rectángulo que ocupa la imagen
        GUIElement.__init__(self, guiScreen, pygame.Rect(0,0,0,0))
        # Se coloca el rectangulo en su posicion
        self.set_position(position)

    def update(self, time):
        return

    def draw(self, screen):
        screen.blit(self.textSurface, self.rect)

    def action(self):
        #No hace nada (es text)
        return

    def change_font(self, font):
        self.font = font
        self.update_text_surface()

    def change_text(self, str):
        self.text = str
        self.update_text_surface()

    def change_color(self, color):
        self.color = color
        self.update_text_surface()

    def update_text_surface(self):
        self.textSurface = self.font.render(self.text, False, self.color)
