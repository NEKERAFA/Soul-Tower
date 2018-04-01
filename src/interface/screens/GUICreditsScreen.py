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
CREDITS_SPRITE_LOCATION = os.path.join(INTERFACE_GAME_FOLDER, 'credits.png')

class GUICreditsScreen(GUIScreen):
    def __init__(self, stage):
        GUIScreen.__init__(self, stage)
        # Texto de muerte
        self.creditsImage = GUIImage(self, CREDITS_SPRITE_LOCATION, (0,SCREEN_HEIGHT), None, None)
        
        # Surface para hacer un fadeout
        self.alpha = 255
        self.black = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

        self.add_element(self.creditsImage)

    def update(self, time):
        GUIScreen.update(self, time)
        self.alpha = max(self.alpha - time*0.1, 0)

    def draw(self, screen):
        GUIScreen.draw(self, screen)
        self.black.set_alpha(int(self.alpha))
        screen.blit(self.black, (0, 0))

    def events(self, event_list):
        return
