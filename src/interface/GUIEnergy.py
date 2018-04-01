# -*- encoding: utf-8 -*-

import pygame
from src.ResourceManager import *
from src.interface.GUIElement import *
from src.interface.GUIChargeBar import *

# -------------------------------------------------
# Clase GUIEnergy
# Representación de las barras de energía

class GUIEnergy(GUIElement):
    def __init__(self, guiScreen, name, position, scale, colorkey=-1):

        # GUI contenedora de la barra
        self.guiScreen = guiScreen

        # String de la imagen de las barras de energía
        self.name = name
        self.scale = scale
        self.colorkey = colorkey

        # Array de barras a dibujar
        self.barArray = []

        # Posicion de los corazones
        self.barPos = position
        bar = None

        # Se llama al método de la clase padre con un rectángulo arbitrario (ya que este objeto no tiene imagen propia)
        GUIElement.__init__(self, pygame.Rect((0,0),(0,0)))
        # Se coloca el rectangulo en su posicion
        self.set_position(position)

        self.inbetween = -5

        self.maxEnergyCounter = self.guiScreen.player.stats["max_nrg"]
        self.energyCounter = self.guiScreen.player.stats["nrg"]
        #self.energyRegen = self.guiScreen.player.stats["nrg_reg"]

        self.currEnergy = self.maxEnergy = self.maxEnergyCounter

        for i in range(0, int(self.maxEnergyCounter)):
            # Crear barra y meterlo en array
            bar = GUIChargeBar(self.name, self.barPos, self.scale, self.colorkey)
            self.barArray.append(bar)
            # Actualizar posiciones del resto de barras
            self.barPos = (self.barPos[0] + bar.image.get_rect().right+self.inbetween, self.barPos[1])

    def update(self, time):

        # Actualizar barras
        i = -1
        for i in range(0, int(self.currEnergy)):
            self.barArray[i].percent = 1.
        for j in range(int(self.currEnergy), self.maxEnergy):
            self.barArray[j].percent = 0.
        if(self.currEnergy - int(self.currEnergy) > 0):
            self.barArray[i+1].percent = self.currEnergy - int(self.currEnergy)


    def draw(self, screen):
        # Dibujar corazones
        for i in range(0, len(self.barArray)):
            self.barArray[i].draw(screen)

    def action(self):
        return

    def gain_energy_bar(self):
        # Crear barra y meterlo en array
        bar = GUIChargeBar(self.name, self.barPos, self.scale, self.colorkey)
        #bar.set_fill_speed(self.energyRegen)
        self.barArray.append(bar)
        # Actualizar posiciones del resto de barras
        self.barPos = (self.barPos[0] + bar.image.get_rect().right+self.inbetween, self.barPos[1])

        self.maxEnergy += 1
        self.currEnergy = self.maxEnergy

    def set_energy(self, value):
        self.currEnergy = value

        # Actualizar energía
        #if(self.currEnergy < self.maxEnergy):
        #    self.currEnergy = min(self.maxEnergy, self.currEnergy + self.energyRegen)
