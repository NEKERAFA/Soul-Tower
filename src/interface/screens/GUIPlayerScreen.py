# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
from src.ResourceManager import *
from src.scenes.Scene import *
from src.interface.screens.GUIScreen import *
from src.interface.GUIHealth import *
from src.interface.GUIEnergy import *
from src.interface.GUIButton import *
from src.interface.GUICharacterSymbol import *
from src.interface.GUIText import *
from src.scenes.stage.InRoomState import *

# -------------------------------------------------
# Clase GUIPlayerScreen
# Interfaz durante el gameplay

# Localización de los sprites
HEART_SPRITE_LOCATION = os.path.join(INTERFACE_PLAYER_FOLDER, 'gui_heart.png')
ENERGY_BAR_SPRITE_LOCATION = os.path.join(INTERFACE_PLAYER_FOLDER, 'gui_energy_bar.png')
SOULS_SPRITE_LOCATION = os.path.join(INTERFACE_PLAYER_FOLDER, 'gui_souls_box.png')

DEFAULT_FONT = 'PixelOperatorHB.ttf'
DEFAULT_FONT_SIZE = 14

class GUIPlayerScreen(GUIScreen):
    def __init__(self, stage):
        GUIScreen.__init__(self, stage)

        self.player = self.stage.player

        font = ResourceManager.load_font(DEFAULT_FONT, DEFAULT_FONT_SIZE)

        #TODO: posiciones y escalas relativas a la pantalla
        self.health = GUIHealth(self, HEART_SPRITE_LOCATION, (55,30), -1)
        self.energy = GUIEnergy(self, ENERGY_BAR_SPRITE_LOCATION, (55,40), None)
        self.charSymb = GUICharacterSymbol(self, (20, 40), None)

        soulsPos = (SCREEN_WIDTH-60, SCREEN_HEIGHT-38)
        self.soulsText = GUIText(self, soulsPos, font, str(self.player.souls), 'right', (255, 255, 255))
        self.soulsSymb = GUIImage(self, SOULS_SPRITE_LOCATION, (soulsPos[0]-40, soulsPos[1]+8))
        # Añadir al array de GUIElements para poder dibujar y actualizar
        self.GUIElements.append(self.health)
        self.GUIElements.append(self.energy)
        self.GUIElements.append(self.charSymb)
        self.GUIElements.append(self.soulsSymb)
        self.GUIElements.append(self.soulsText)


    def events(self, event_list):
        #for event in event_list:
        #    if event.type == KEYDOWN and event.key == pygame.K_e:
        #        self.charSymb.action()
        return
