# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
from src.ResourceManager import *
from src.scenes.Scene import *
from src.interface.GUIScreen import *
from src.interface.GUIImage import *
from src.interface.GUIChargeBar import *
from src.interface.GUIDialog import *

# -------------------------------------------------
# Clase GUIPlayerScreen
# Interfaz durante el gameplay

class GUIPlayerScreen(GUIScreen):
    def __init__(self):
        GUIScreen.__init__(self)
        #TODO: posiciones y escalas relativas a la pantalla
        #TODO: bucle for para cada corazón/barra de estamina
        self.heart = GUIImage(self, "interface/player/heart_placeholder.png", (20,20), (20,20))
        self.stamina = GUIChargeBar(self, "interface/player/stamina_placeholder.png", (20,40), (30,10))
        self.dialogBox = GUIDialog(self, "interface/game/dialog_placeholder.png", (20,400), (300, 200), "this is a text string")

        self.GUIElements.append(self.heart)
        self.GUIElements.append(self.stamina)
        self.GUIElements.append(self.dialogBox)
    def events(self, event_list):
        GUIScreen.events(self, event_list)
    def draw(self, screen):
        GUIScreen.draw(self, screen)
