# -*- encoding: utf-8 -*-

import pygame
from pygame.locals import *
from src.ResourceManager import *
from src.scenes.Scene import *

# -------------------------------------------------
# Clase GUIScreen
# La clase GUIScreen no hereda de Screen, ya que no tiene imagen propia a dibujar
# TODO: maybe hacer que GUIScreen y Screen hereden de la misma clase (¿una "superscreen"?)
class GUIScreen(object):
    def __init__(self):
        # Se tiene una lista de elementos GUI
        self.GUIElements = []
        # Se tiene una lista de animaciones
        #self.animations = []

    def events(self, event_list):
        for event in event_list:
            if event.type == MOUSEBUTTONDOWN:
                self.elementClick = None
                for element in self.GUIElements:
                    if element.positionIsInElement(event.pos):
                        self.elementClick = element
            if event.type == MOUSEBUTTONUP:
                for element in self.GUIElements:
                    if element.positionIsInElement(event.pos):
                        if (element == self.elementClick):
                            element.action()
    def update(self, time):
        for element in self.GUIElements:
            element.update(time)

    def draw(self, screen):
        # Dibujamos las animaciones
        #for animation in self.animations:
        #    animation.draw(screen)
        # Después los botones
        for element in self.GUIElements:
            element.draw(screen)
