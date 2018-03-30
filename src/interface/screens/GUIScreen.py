# -*- encoding: utf-8 -*-

import pygame
from pygame.locals import *
from src.ResourceManager import *
from src.scenes.Scene import *

# -------------------------------------------------
# Clase GUIScreen
# La clase GUIScreen no hereda de Screen, ya que no tiene imagen propia a dibujar

INTERFACE_PLAYER_FOLDER = os.path.join('interface', 'player')
INTERFACE_GAME_FOLDER = os.path.join('interface', 'game')

class GUIScreen(object):
    def __init__(self, stage):
        # Se tiene una lista de elementos GUI
        self.GUIElements = []
        # Se tiene una lista de animaciones
        #self.animations = []

        self.stage = stage

    # TODO añadir a UML
    def add_element(self, element):
        self.GUIElements.append(element)
    # TODO añadir a UML
    def remove_element(self, element):
        self.GUIElements.remove(element)

    def events(self, event_list):
        raise NotImplemented("Tiene que implementar el metodo events.")

    def update(self, time):
        #Actualizar los elementos de la interfaz
        for element in self.GUIElements:
            element.update(time)

    def draw(self, screen):
        # Dibujamos las animaciones
        #for animation in self.animations:
        #    animation.draw(screen)
        # Después los botones
        for element in self.GUIElements:
            element.draw(screen)
