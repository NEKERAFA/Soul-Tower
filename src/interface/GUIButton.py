# -*- encoding: utf-8 -*-

import pygame
from src.ResourceManager import *
from src.interface.GUIElement import *

# -------------------------------------------------
# Clase GUIButton

class GUIButton(GUIElement):
    def __init__(self, gui_screen, name, position, scale):
        #cargar imagen
        self.image = ResourceManager.load_image(name, -1)
        #cambiar escala
        self.image = pygame.transform.scale(self.image, scale)
        # Se llama al método de la clase padre con el rectángulo que ocupa el botón
        GUIElement.__init__(self, gui_screen, self.image.get_rect())
        # Se coloca el rectangulo en su posicion
        self.set_position(position)

    def update(self, time):
        #TODO: cambiar imagen/estado del botón (pulsado/no pulsado)
        return

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def action(self):
        raise NotImplemented("Tiene que implementar el metodo acción.")
