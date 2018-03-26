# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
from src.ResourceManager import *
from src.scenes.Scene import *
from src.interface.screens.GUIScreen import *
from src.interface.GUITutorialImage import *
from src.interface.GUIText import *
from src.scenes.Stage import *

# -------------------------------------------------
# Clase GUITutorialScreen
# Interfaz en la primera sala

# Localización de los sprites
W_SPRITE_LOCATION = os.path.join('interface', 'game', 'tutorial', 'w_placeholder.png')
A_SPRITE_LOCATION = os.path.join('interface', 'game', 'tutorial', 'a_placeholder.png')
S_SPRITE_LOCATION = os.path.join('interface', 'game', 'tutorial', 's_placeholder.png')
D_SPRITE_LOCATION = os.path.join('interface', 'game', 'tutorial', 'd_placeholder.png')
E_SPRITE_LOCATION = os.path.join('interface', 'game', 'tutorial', 'e_placeholder.png')

class GUITutorialScreen(GUIScreen):
    def __init__(self, stage):
        GUIScreen.__init__(self)

        self.stage = stage
        # Contador para eliminar texto según se vayan pulsando las teclas
        self.tutorialKeyCounter = 0
        font = ResourceManager.load_font(DEFAULT_FONT, DEFAULT_FONT_SIZE)

        # Movimiento
        self.movementText = GUIText(self, (120, 60), font, 'Movement keys', 'center')
        wKey = GUITutorialImage(self, W_SPRITE_LOCATION, (100,100), (40,40), pygame.K_w)
        aKey = GUITutorialImage(self, A_SPRITE_LOCATION, (60,140), (40,40), pygame.K_a)
        sKey = GUITutorialImage(self, S_SPRITE_LOCATION, (100,140), (40,40), pygame.K_s)
        dKey = GUITutorialImage(self, D_SPRITE_LOCATION, (140,140), (40,40), pygame.K_d)

        self.onDialogue = False
        self.dialogue1 = 'test.json'

        # Cambio de personaje
        self.eKey = GUITutorialImage(self, E_SPRITE_LOCATION, (140,100), (40,40), pygame.K_e)
        self.swapText = GUIText(self, (120, 60), font, 'Swap character', 'center')

        # TODO Ataque
        # TODO Dash

        self.add_element(wKey)
        self.add_element(aKey)
        self.add_element(sKey)
        self.add_element(dKey)
        self.add_element(self.movementText)

    def update(self, time):
        GUIScreen.update(self, time)
        if self.onDialogue and type(self.stage.state) is not OnDialogueState:
            self.onDialogue = False
            self.nextElement()

    def events(self, event_list):
        if not self.onDialogue:
            for event in event_list:
                if event.type == pygame.KEYDOWN:
                    for element in self.GUIElements:
                        if (element.__class__.__name__ == 'GUITutorialImage' and element.associatedKey == event.key):
                            element.action()
                            self.tutorialKeyCounter += 1
                            # Si se han pulsado las teclas de movimiento se elimina el texto y se añaden los siguientes elementos
                            if(self.tutorialKeyCounter == 4):
                                self.remove_element(self.movementText)
                                # Diálogo intermedio
                                self.stage.setState(OnDialogueState(self.dialogue1, self.stage))
                                self.onDialogue = True
                            elif(self.tutorialKeyCounter == 5):
                                self.remove_element(self.swapText)

    def nextElement(self):
        if self.tutorialKeyCounter == 4:
            self.add_element(self.eKey)
            self.add_element(self.swapText)
        #elif self.tutorialKeyCounter == 5:
            # TODO añadir
