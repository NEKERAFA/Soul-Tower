# -*- encoding: utf-8 -*-

import pygame
from src.ResourceManager import *
from src.interface.GUIElement import *

# -------------------------------------------------
# Clase GUIImage

class GUIImage(GUIElement):
    def __init__(self, gui_screen, name, position, scale, colorkey=-1):
        #cargar imagen con transparencia
        self.image = ResourceManager.load_image(name, colorkey)
        #cambiar escala
        self.image = pygame.transform.scale(self.image, scale)
        # Se llama al método de la clase padre con el rectángulo que ocupa la imagen
        GUIElement.__init__(self, gui_screen, self.image.get_rect())
        # Se coloca el rectangulo en su posicion
        self.set_position(position)

    def update(self, time):
        return

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def action(self):
        #No hace nada (es una imagen)
        return
