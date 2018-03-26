# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
from src.ResourceManager import *
from src.scenes.Scene import *
from src.interface.screens.GUIScreen import *
from src.interface.GUIHealth import *
from src.interface.GUIChargeBar import *
from src.interface.GUIDialog import *
from src.interface.GUIButton import *
from src.interface.GUIText import *
from src.interface.GUICharacterSymbol import *

# -------------------------------------------------
# Clase GUIPlayerScreen
# Interfaz durante el gameplay

# Localización de los sprites
HEART_SPRITE_LOCATION = 'interface/player/heart_placeholder.png'
STAMINA_BAR_SPRITE_LOCATION = 'interface/player/stamina_placeholder.png'


class GUIPlayerScreen(GUIScreen):
    def __init__(self):
        GUIScreen.__init__(self)
        #TODO: posiciones y escalas relativas a la pantalla
        #TODO: bucle for para cada corazón/barra de estamina
        self.health = GUIHealth(self, HEART_SPRITE_LOCATION, (20,20), (20,20), 3)
        self.stamina = GUIChargeBar(self, STAMINA_BAR_SPRITE_LOCATION, (20,40), (30,10))
        self.charSymb = GUICharacterSymbol(self, (20, 230), (30, 30))

        #button = GUIButton(self, "interface/player/button_up_placeholder.png", "interface/player/button_down_placeholder.png", (0,0), (40,40))
        #text = GUIText(self, (200, 20), pygame.font.SysFont('dejavusans', 14))
        # TODO dialogBox = GUIDialog(self, "interface/game/dialog_placeholder.png", (20,295), (360, 100), pygame.font.SysFont('dejavusans', 14), "this is a text string", 0.04)
        # TODO recolocar diálogo
        #text.change_text('test')
        #text.change_color((255, 0, 0))
        #text.change_font(pygame.font.SysFont('dejavusans', 30))

        # Añadir al array de GUIElements para poder dibujar y actualizar
        self.GUIElements.append(self.health)
        self.GUIElements.append(self.stamina)
        self.GUIElements.append(self.charSymb)
