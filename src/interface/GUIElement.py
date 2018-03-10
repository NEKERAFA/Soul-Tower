# -*- encoding: utf-8 -*-

import pygame

# -------------------------------------------------
# Clase abstracta GUIElement

class GUIElement(object):
    def __init__(self, guiScreen, rect):
        self.guiScreen = guiScreen
        self.rect = rect

    def set_position(self, position):
        (positionX, positionY) = position
        self.rect.left = positionX
        self.rect.bottom = positionY

    #Devuelve si la posición pasada como argumento (generalmente la del ratón) está encima del elemento o no
    def position_is_in_element(self, position):
        (positionX, positionY) = position
        if (positionX>=self.rect.left) and (positionX<=self.rect.right) and (positionY>=self.rect.top) and (positionY<=self.rect.bottom):
            return True
        else:
            return False

    def update(self, time):
        raise NotImplemented("Tiene que implementar el metodo update.")
    def draw(self):
        raise NotImplemented("Tiene que implementar el metodo draw.")
    def action(self):
        raise NotImplemented("Tiene que implementar el metodo action.")
