# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
from src.ResourceManager import *
from src.scenes.Scene import *
from src.interface.screens.GUIScreen import *
from src.interface.screens.GUIButtonContainer import *
from src.interface.GUIButton import *

# -------------------------------------------------
# Clase GUIMenuScreen
# Interfaz durante los menús

# Localización de los sprites


class GUIMenuScreen(GUIScreen):
    def __init__(self, stage):
        GUIScreen.__init__(self, stage)


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
