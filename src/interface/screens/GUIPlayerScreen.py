# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
from src.ResourceManager import *
from src.scenes.Scene import *
from src.interface.screens.GUIScreen import *
from src.interface.GUIHealth import *
from src.interface.GUIChargeBar import *
from src.interface.GUIButton import *
from src.interface.GUICharacterSymbol import *

# -------------------------------------------------
# Clase GUIPlayerScreen
# Interfaz durante el gameplay

# Localización de los sprites
HEART_SPRITE_LOCATION = 'interface/player/heart_placeholder.png'
STAMINA_BAR_SPRITE_LOCATION = 'interface/player/stamina_placeholder.png'


class GUIPlayerScreen(GUIScreen):
    def __init__(self, stage):
        GUIScreen.__init__(self, stage)

        #print(self.stage.__class__.__name__)
        #print(self.stage.stageNum)
        self.player = self.stage.player

        #TODO: posiciones y escalas relativas a la pantalla
        #TODO: bucle for para cada corazón/barra de estamina
        self.health = GUIHealth(self, HEART_SPRITE_LOCATION, (20,20), (20,20), 3)
        self.stamina = GUIChargeBar(self, STAMINA_BAR_SPRITE_LOCATION, (20,40), (30,10))
        self.charSymb = GUICharacterSymbol(self, (20, 230), (30, 30))

        # Añadir al array de GUIElements para poder dibujar y actualizar
        self.GUIElements.append(self.health)
        self.GUIElements.append(self.stamina)
        self.GUIElements.append(self.charSymb)

    def events(self, event_list):
        for event in event_list:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                for element in self.GUIElements:
                    if element.__class__.__name__ == 'GUICharacterSymbol':
                        self.elementClick = element
                        element.action()
