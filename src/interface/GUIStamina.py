# -*- encoding: utf-8 -*-

import pygame
from src.ResourceManager import *
from src.interface.GUIElement import *
from src.interface.GUIChargeBar import *

# -------------------------------------------------
# Clase GUIStamina
# Representación de las barras de estamina / energía

class GUIStamina(GUIElement):
    def __init__(self, guiScreen, name, position, scale, colorkey=-1):

        # String de la imagen de las barras de estamina
        self.name = name
        self.scale = scale
        self.colorkey = colorkey

        # Array de barras a dibujar
        self.barArray = []

        # Posicion de los corazones
        self.barPos = position
        bar = None

        # Se llama al método de la clase padre con un rectángulo arbitrario (ya que este objeto no tiene imagen propia)
        GUIElement.__init__(self, guiScreen, pygame.Rect((0,0),(0,0)))
        # Se coloca el rectangulo en su posicion
        self.set_position(position)

        self.maxStaminaCounter = self.guiScreen.player.stats["max_nrg"]
        self.staminaCounter = self.guiScreen.player.stats["nrg"]
        self.staminaRegen = self.guiScreen.player.stats["nrg_reg"]

        self.currStamina = self.maxStamina = self.maxStaminaCounter

        for i in range(0, int(self.maxStaminaCounter)):
            # Crear barra y meterlo en array
            bar = GUIChargeBar(self.guiScreen, self.name, self.barPos, self.scale, self.colorkey)
            self.barArray.append(bar)
            # Actualizar posiciones del resto de barras
            self.barPos = (self.barPos[0] + bar.image.get_rect().right+2, self.barPos[1])

    def update(self, time):
        # Actualizar estamina
        # TODO esto se podría gestionar tomando los datos directamente del jugador
        if(self.currStamina < self.maxStamina):
            self.currStamina = min(self.maxStamina, self.currStamina + time*self.staminaRegen)

        # Actualizar barras
        i = -1
        for i in range(0, int(self.currStamina)):
            self.barArray[i].percent = 1.
        for j in range(int(self.currStamina), self.maxStamina):
            self.barArray[j].percent = 0.
        if(self.currStamina - int(self.currStamina) > 0):
            self.barArray[i+1].percent = self.currStamina - int(self.currStamina)


    def draw(self, screen):
        # Dibujar corazones
        for i in range(0, len(self.barArray)):
            self.barArray[i].draw(screen)

    def action(self):
        return

    def gain_stamina_bar(self):
        # Crear barra y meterlo en array
        bar = GUIChargeBar(self.guiScreen, self.name, self.barPos, self.scale, self.colorkey)
        bar.set_fill_speed(self.staminaRegen)
        self.barArray.append(bar)
        # Actualizar posiciones del resto de barras
        self.barPos = (self.barPos[0] + bar.image.get_rect().right+2, self.barPos[1])

    def lose_stamina(self, quantity):
        if(quantity <= self.currStamina):
            self.currStamina -= quantity
