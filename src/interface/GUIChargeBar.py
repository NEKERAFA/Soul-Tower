# -*- encoding: utf-8 -*-

import pygame
from src.ResourceManager import *
from src.interface.GUIElement import *

# -------------------------------------------------
# Clase GUIChargeBar

class GUIChargeBar(GUIElement):
    def __init__(self, gui_screen, name, position, scale):
        #cargar imagen
        self.image = ResourceManager.load_image(name, -1)
        #cambiar escala
        self.image = pygame.transform.scale(self.image, scale)
        # Se llama al método de la clase padre con el rectángulo que ocupa el botón
        GUIElement.__init__(self, gui_screen, self.image.get_rect())
        # Se coloca el rectangulo en su posicion
        self.set_position(position)
        self.percent = 1.
        self.speed = 1./1000. # 100% de la barra/1000ms = 100% en 1s

    def update(self, time):
        #TODO: esta "recarga" se debería tener en cuenta en el propio personaje, y
        # habría que obtener el valor a representar a partir de él.
        if(self.percent < 1.):
            self.percent = min(1., self.percent+time*self.speed)
        else:
            self.percent = 0

    def draw(self, screen):
        width = self.image.get_width()
        subs = self.image.subsurface((0,0,self.percent*width, self.image.get_height()))
        screen.blit(subs, self.rect)

    def action(self):
        #No hace nada (es una imagen)
        return
