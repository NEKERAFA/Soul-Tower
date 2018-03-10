# -*- encoding: utf-8 -*-

import pygame
from src.ResourceManager import *
from src.interface.GUIImage import *

# -------------------------------------------------
# Clase GUIButton

class GUIButton(GUIImage):
    def __init__(self, gui_screen, name, position, scale):
        
        # Se llama al método de la clase padre con el rectángulo que ocupa el botón
        GUIImage.__init__(self, gui_screen, name, position, scale)
        # Se coloca el rectangulo en su posicion
        self.set_position(position)

    def update(self, time):
        #TODO: cambiar imagen/estado del botón (pulsado/no pulsado)
        return

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def action(self):
        raise NotImplemented("Tiene que implementar el metodo acción.")
