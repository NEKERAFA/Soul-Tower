# -*- encoding: utf-8 -*-

import pygame
from src.ResourceManager import *
from src.interface.GUIImage import *

# -------------------------------------------------
# Clase GUIChargeBar

class GUIChargeBar(GUIImage):
    def __init__(self, name, position, scale, colorkey=-1):
        # La imagen se carga sin transparencias
        GUIImage.__init__(self, name, position, scale, colorkey)

        # Porcentaje de rellenado de la barra; 1 -> la barra se dibuja por completo
        self.percent = 1.
        # Velocidad de llenado de la barra: 100% de la barra/1000ms = 100% en 1s
        self.speed = 0

        self.recharge = False


    def update(self, time):
        # Recargar barra
        if(self.percent < 1. and self.recharge):
            self.percent = min(1., self.percent+time*self.speed)

    def draw(self, screen):
        # Obtenemos ancho de la imagen (barra)
        width = self.image.get_width()
        # Calculamos la subsuperficie a dibujar; si el porcentaje es 1, es igual a la superficie de la imagen
        subs = self.image.subsurface((0,0,self.percent*width, self.image.get_height()))
        # Dibujamos la subsuperficie
        screen.blit(subs, self.rect)

    def action(self):
        # No hace nada
        return

    def gain_charge(self, value):
        # Aumentar tamaño de la barra
        # value es un valor entre 0 y 1
        self.percent = min(1., self.percent + value)

    def lose_charge(self, value):
        # Disminuir tamaño de la barra
        # value es un valor entre 0 y 1
        self.percent = max(0., self.percent - value)

    def set_fill_speed(self, speed):
        # Cambiar velocidad de carga de la barra
        self.speed = speed
