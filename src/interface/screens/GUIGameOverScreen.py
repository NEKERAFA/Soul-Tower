# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
from src.ResourceManager import *
from src.interface.screens.GUIScreen import *
from src.interface.GUIImage import *

# -------------------------------------------------
# Clase GUIGameOverScreen
# Pantalla que aparece al morir

# Localización de los sprites
GAME_OVER_TEXT_LOCATION = os.path.join(INTERFACE_GAME_FOLDER, 'gui_game_over_text.png')
DEAD_CHARACTER_SPRITE_LOCATION = os.path.join(INTERFACE_GAME_FOLDER, 'gui_dead_character_sprite.png')

#DEFAULT_FONT = 'PixelOperatorHB.ttf'
#DEFAULT_FONT_SIZE = 12

class GUIGameOverScreen(GUIScreen):
    def __init__(self, stage):
        GUIScreen.__init__(self, stage)
        # Texto de muerte
        self.game_over_text = GUIImage(self, GAME_OVER_TEXT_LOCATION, (0,SCREEN_HEIGHT/2))

        # Sprite del personaje muerto
        self.dead_character = GUIImage(self, DEAD_CHARACTER_SPRITE_LOCATION, (SCREEN_WIDTH/2-20, SCREEN_HEIGHT/2+70))

        # Surface para hacer un fadeout
        self.alpha = 0
        self.black = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

        self.add_element(self.game_over_text)
        self.add_element(self.dead_character)

    def update(self, time):
        GUIScreen.update(self, time)
        self.alpha = min(self.alpha + time*0.1, 255)

    def draw(self, screen):
        self.black.set_alpha(int(self.alpha))
        screen.blit(self.black, (0, 0))
        GUIScreen.draw(self, screen)

    def events(self, event_list):
        return
