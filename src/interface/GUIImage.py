# -*- encoding: utf-8 -*-

import pygame
from src.ResourceManager import *
from src.interface.GUIElement import *

# -------------------------------------------------
# Clase GUIImage

class GUIImage(GUIElement):
    def __init__(self, gui_screen, name, position):
        #cargar imagen
        self.image = ResourceManager.load_image(name, -1)
        #cambiar escala
        self.image = pygame.transform.scale(self.image, (20,20))
        # Se llama al método de la clase padre con el rectángulo que ocupa el botón
        GUIElement.__init__(self, gui_screen, self.image.get_rect())
        # Se coloca el rectangulo en su posicion
        self.setPosition(position)
    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def action(self):
        #No hace nada (es una imagen)
        return
