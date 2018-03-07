# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
from src.ResourceManager import *
from src.scenes.Scene import *
from src.interface.GUIScreen import *
from src.interface.GUIImage import *

# -------------------------------------------------
# Clase GUIPlayerScreen
# Interfaz durante el gameplay

class GUIPlayerScreen(GUIScreen):
    def __init__(self):
        GUIScreen.__init__(self)
        self.heart = GUIImage(self, "interface/player/heart_placeholder.png", (20,20))
        self.GUIElements.append(self.heart)
    def events(self, event_list):
        GUIScreen.events(self, event_list)
    def draw(self, screen):
        GUIScreen.draw(self, screen)
