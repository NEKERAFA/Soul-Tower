# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
from src.ResourceManager import *
from src.scenes.Stage import *
from src.interface.screens.GUIScreen import *
from src.interface.GUIImage import *
from src.interface.GUIButton import *


# -------------------------------------------------
# Clase GUICreditsScreen
# Pantalla que aparece al terminar el juego

# Localización de los sprites
#GAME_OVER_TEXT_LOCATION = os.path.join(INTERFACE_GAME_FOLDER, 'gui_game_over_text.png')

class GUICreditsScreen(GUIScreen):
    def __init__(self, stage):
        GUIScreen.__init__(self, stage)
        # Texto de muerte
        self.gameOverText = GUIImage(self, GAME_OVER_TEXT_LOCATION, (0,SCREEN_HEIGHT/2-50))

        # Surface para hacer un fadeout
        self.alpha = 0
        self.black = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

        #self.add_element(self.gameOverText)

    def update(self, time):
        GUIScreen.update(self, time)
        self.alpha = min(self.alpha + time*0.1, 255)

    def draw(self, screen):
        self.black.set_alpha(int(self.alpha))
        screen.blit(self.black, (0, 0))
        GUIScreen.draw(self, screen)

    def events(self, event_list):
        return
