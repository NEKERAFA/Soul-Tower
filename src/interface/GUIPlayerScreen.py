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
        heart = GUIImage(self, "interface/player/heart_placeholder.png", (20,20), (20,20))
        stamina = GUIChargeBar(self, "interface/player/stamina_placeholder.png", (20,40), (30,10))
        dialogBox = GUIDialog(self, "interface/game/dialog_placeholder.png", (20,295), (360, 100), pygame.font.SysFont('dejavusans', 14), "this is a text string", 0.04)
        # TODO recolocar diálogo

        self.GUIElements.append(heart)
        self.GUIElements.append(stamina)
        self.GUIElements.append(dialogBox)

    def events(self, event_list):
        GUIScreen.events(self, event_list)

    def draw(self, screen):
        GUIScreen.draw(self, screen)
