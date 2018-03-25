# -*- encoding: utf-8 -*-

import pygame
from pygame.locals import *
from src.ResourceManager import *
from src.scenes.Scene import *

# -------------------------------------------------
# Clase GUIScreen
# La clase GUIScreen no hereda de Screen, ya que no tiene imagen propia a dibujar

class GUIScreen(object):
    def __init__(self):
        # Se tiene una lista de elementos GUI
        self.GUIElements = []
        # Se tiene una lista de animaciones
        #self.animations = []

    # TODO añadir a UML
    def add_element(self, element):
        self.GUIElements.append(element)
    # TODO añadir a UML
    def remove_element(self, element):
        self.GUIElements.remove(element)

    def events(self, event_list):
        for event in event_list:
            if event.type == MOUSEBUTTONDOWN:
                self.elementClick = None
                for element in self.GUIElements:
                    if element.__class__.__name__ == 'GUIButton' and element.position_is_in_element((event.pos[0]/SCALE_FACTOR, event.pos[1]/SCALE_FACTOR)):
                        self.elementClick = element
                        element.action()
            if event.type == MOUSEBUTTONUP:
                for element in self.GUIElements:
                    if element.__class__.__name__ == 'GUIButton' and element.position_is_in_element((event.pos[0]/SCALE_FACTOR, event.pos[1]/SCALE_FACTOR)):
                        if (element == self.elementClick):
                            element.action()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                for element in self.GUIElements:
                    if element.__class__.__name__ == 'GUICharacterSymbol':
                        self.elementClick = element
                        element.action()

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
