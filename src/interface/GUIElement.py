# -*- encoding: utf-8 -*-

import pygame

# -------------------------------------------------
# Clase abstracta GUIElement

class GUIElement:
    def __init__(self, gui_screen, rect):
        self.gui_screen = gui_screen
        self.rect = rect

    def setPosition(self, position):
        (positionX, positionY) = position
        self.rect.left = positionX
        self.rect.bottom = positionY

    #Devuelve si la posición pasada como argumento (generalmente la del ratón) está encima del elemento o no
    def positionIsInElement(self, position):
        (positionX, positionY) = position
        if (positionX>=self.rect.left) and (positionX<=self.rect.right) and (positionY>=self.rect.top) and (positionY<=self.rect.bottom):
            return True
        else:
            return False

    def draw(self):
        raise NotImplemented("Tiene que implementar el metodo draw.")
    def action(self):
        raise NotImplemented("Tiene que implementar el metodo action.")
