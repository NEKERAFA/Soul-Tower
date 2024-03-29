# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
from src.ResourceManager import *
from src.scenes.Stage import *
from src.interface.screens.GUIScreen import *
from src.interface.GUIImage import *
from src.interface.GUIButton import *
from src.interface.GUIText import *


# -------------------------------------------------
# Clase GUICreditsScreen
# Pantalla que aparece al terminar el juego

# Localización de los sprites
CREDITS_SPRITE_LOCATION = os.path.join(INTERFACE_GAME_FOLDER, 'soul_tower_background.png')
SOUL_TOWER_SPRITE_LOCATION = os.path.join(INTERFACE_GAME_FOLDER, 'soul_tower_text.png')

DEFAULT_FONT = 'PixelOperatorHB.ttf'
DEFAULT_FONT_SIZE = 16

class GUICreditsScreen(GUIScreen):
    def __init__(self, stage):
        GUIScreen.__init__(self, stage)
        # Fondo
        self.creditsImage = GUIImage(CREDITS_SPRITE_LOCATION, (0,SCREEN_HEIGHT), None, None)
        self.add_element(self.creditsImage)

        # Título
        self.soulTowerImage = GUIImage(SOUL_TOWER_SPRITE_LOCATION, (SCREEN_WIDTH/2,SCREEN_HEIGHT-50))

        self.add_element(self.soulTowerImage)

        # Texto de créditos
        creditsContent = [u"Rafael Alcalde Azpiazu", u"Diego Martínez Cela", u"Eva Suárez García", u"Iago Otero Coto", u"Jorge Viteri Letamendía"]
        self.creditsContents = []
        font = ResourceManager.load_font(DEFAULT_FONT, DEFAULT_FONT_SIZE)
        for i in range(0, len(creditsContent)):
            creditsText = GUIText((SCREEN_WIDTH/2,SCREEN_HEIGHT+15*i), font, creditsContent[i],'center', (255, 255, 255))
            self.creditsContents.append(creditsText)
            self.GUIElements.append(creditsText)

        # Surface para hacer un fadeout
        self.alpha = 255
        self.black = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.adder = 0

    def update(self, time):
        GUIScreen.update(self, time)
        self.alpha = max(self.alpha - time*0.1, 0)

        self.adder = min(1, self.adder+time*0.02)
        if(self.soulTowerImage.rect.top) > 10:
            for i in range(0, len(self.creditsContents)):
                pos = self.creditsContents[i].rect.midbottom
                self.creditsContents[i].rect.midbottom = (pos[0], pos[1]-self.adder)
            self.soulTowerImage.rect.midbottom = (SCREEN_WIDTH/2, self.soulTowerImage.rect.midbottom[1]-self.adder)
    def draw(self, screen):
        GUIScreen.draw(self, screen)
        self.black.set_alpha(int(self.alpha))
        screen.blit(self.black, (0, 0))

    def events(self, event_list):
        return
