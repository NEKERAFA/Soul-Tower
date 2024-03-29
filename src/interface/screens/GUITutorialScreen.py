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
W_SPRITE_LOCATION = os.path.join(INTERFACE_GAME_FOLDER, 'tutorial', 'gui_w_key.png')
A_SPRITE_LOCATION = os.path.join(INTERFACE_GAME_FOLDER, 'tutorial', 'gui_a_key.png')
S_SPRITE_LOCATION = os.path.join(INTERFACE_GAME_FOLDER, 'tutorial', 'gui_s_key.png')
D_SPRITE_LOCATION = os.path.join(INTERFACE_GAME_FOLDER, 'tutorial', 'gui_d_key.png')
E_SPRITE_LOCATION = os.path.join(INTERFACE_GAME_FOLDER, 'tutorial', 'gui_e_key.png')
SPACE_SPRITE_LOCATION = os.path.join(INTERFACE_GAME_FOLDER, 'tutorial', 'gui_space_key.png')
Q_SPRITE_LOCATION = os.path.join(INTERFACE_GAME_FOLDER, 'tutorial', 'gui_q_key.png')
MOUSE_SPRITE_LOCATION = os.path.join(INTERFACE_GAME_FOLDER, 'tutorial', 'gui_mouse_button.png')

class GUITutorialScreen(GUIScreen):
    def __init__(self, stage):
        GUIScreen.__init__(self, stage)

        # Referencia a la puerta del final de tutorial, le ponemos una llave falsa
        self.tutorialDoor = stage.rooms[0].unlockedDoors[0]
        self.tutorialDoor.key = ""

        # Contador para eliminar texto según se vayan pulsando las teclas
        self.tutorialKeyCounter = 0
        font = ResourceManager.load_font(DEFAULT_FONT, DEFAULT_FONT_SIZE)

        # Movimiento
        self.movementText = GUIText((120, 60), font, 'Moverse', 'center')
        wKey = GUITutorialImage(self, W_SPRITE_LOCATION, (100,100), (40,40), pygame.K_w)
        aKey = GUITutorialImage(self, A_SPRITE_LOCATION, (60,140), (40,40), pygame.K_a)
        sKey = GUITutorialImage(self, S_SPRITE_LOCATION, (100,140), (40,40), pygame.K_s)
        dKey = GUITutorialImage(self, D_SPRITE_LOCATION, (140,140), (40,40), pygame.K_d)

        self.add_element(wKey)
        self.add_element(aKey)
        self.add_element(sKey)
        self.add_element(dKey)
        self.add_element(self.movementText)

        self.onDialogue = False
        self.dialogues = ['movement.json', 'exitTutorial.json']
        self.dialogueIndex = 0

        # Cambio de personaje
        self.eKey = GUITutorialImage(self, E_SPRITE_LOCATION, (140,100), (40,40), pygame.K_e)
        self.swapText = GUIText((120, 60), font, 'Cambiar de personaje', 'center')

        # Dash/Defender
        self.spaceKey = GUITutorialImage(self, SPACE_SPRITE_LOCATION, (100,250), (200,50), pygame.K_SPACE)
        self.dashText = GUIText((200, 200), font, 'Defenderse (Daric)/Sprint (Leraila)', 'center')

        # Ataque
        self.mouse = GUITutorialImage(self, MOUSE_SPRITE_LOCATION, (250, 100), None, None, -1)
        self.attackText = GUIText((275, 120), font, 'Atacar', 'center')

        # Interactuar
        self.qKey = GUITutorialImage(self, Q_SPRITE_LOCATION, (75, 100), (40, 40), pygame.K_q)
        self.actionText = GUIText((100, 60), font, 'Interactuar', 'center')

    def update(self, time):
        GUIScreen.update(self, time)
        if self.onDialogue and type(self.stage.state) is not OnDialogueState:
            self.onDialogue = False
            self.next_element()

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
                                self.stage.set_state(OnDialogueState(self.dialogues[self.dialogueIndex], self.stage))
                                self.dialogueIndex += 1
                                self.onDialogue = True
                            elif(self.tutorialKeyCounter == 5):
                                self.remove_element(self.swapText)
                                self.next_element()
                            elif(self.tutorialKeyCounter == 6):
                                self.remove_element(self.dashText)
                                self.next_element()
                                #TODO: si pulsas dos veces rápido la barra espaciadora el juego se queda atascado en este punto
                                # Esto se debe a que la llamada a events no está sincronizada
                            elif self.tutorialKeyCounter == 9:
                                self.remove_element(self.actionText)
                elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                    if self.tutorialKeyCounter == 7:
                        self.tutorialKeyCounter += 1
                        self.mouse.action()
                        self.remove_element(self.attackText)
                        self.stage.set_state(OnDialogueState(self.dialogues[self.dialogueIndex], self.stage))
                        self.dialogueIndex += 1
                        self.onDialogue = True

    def next_element(self):
        if self.tutorialKeyCounter == 4:
            self.add_element(self.eKey)
            self.add_element(self.swapText)
        elif self.tutorialKeyCounter == 5:
            self.add_element(self.spaceKey)
            self.add_element(self.dashText)
        elif self.tutorialKeyCounter == 6:
            self.add_element(self.mouse)
            self.add_element(self.attackText)
            self.tutorialKeyCounter += 1
        elif self.tutorialKeyCounter == 8:
            self.add_element(self.qKey)
            self.add_element(self.actionText)
            self.tutorialDoor.key = None
