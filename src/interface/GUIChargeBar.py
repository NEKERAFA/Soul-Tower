# -*- encoding: utf-8 -*-

import pygame
from src.ResourceManager import *
from src.interface.GUIImage import *

# -------------------------------------------------
# Clase GUIChargeBar

class GUIChargeBar(GUIImage):
    def __init__(self, gui_screen, name, position, scale):
        self.colorkey = None
        # La imagen se carga sin transparencias
        GUIImage.__init__(self, gui_screen, name, position, scale, self.colorkey)

        # Porcentaje de rellenado de la barra; 1 -> la barra se dibuja por completo
        self.percent = 1.
        self.speed = 1./1000. # 100% de la barra/1000ms = 100% en 1s

    def update(self, time):
        #TODO: esta "recarga" se debería tener en cuenta en el propio personaje, y
        # habría que obtener el valor a representar a partir de él.
        if(self.percent < 1.):
            self.percent = min(1., self.percent+time*self.speed)
        #else:
        #    self.percent = 0

    def draw(self, screen):
        #obtenemos ancho de la imagen (barra)
        width = self.image.get_width()
        #calculamos la subsuperficie a dibujar; si el porcentaje es 1, es igual a la superficie de la imagen
        subs = self.image.subsurface((0,0,self.percent*width, self.image.get_height()))
        #dibujamos la subsuperficie
        screen.blit(subs, self.rect)

    def action(self):
        #No hace nada
        return
