# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
from src.ResourceManager import *
from src.scenes.Scene import *
from src.interface.screens.GUIScreen import *
from src.interface.GUIButton import *
from src.sprites.MyStaticAnimatedSprite import *

# -------------------------------------------------
# Clase GUIMainMenuScreen
# Interfaz durante el menú de inicio

# Localización de los sprites
MENU_START_BUTTON_UP_LOCATION = os.path.join(INTERFACE_GAME_FOLDER, 'start_up.png')
MENU_START_BUTTON_DOWN_LOCATION = os.path.join(INTERFACE_GAME_FOLDER, 'start_down.png')
MENU_EXIT_BUTTON_UP_LOCATION = os.path.join(INTERFACE_GAME_FOLDER, 'exit_up.png')
MENU_EXIT_BUTTON_DOWN_LOCATION = os.path.join(INTERFACE_GAME_FOLDER, 'exit_down.png')

class GUIMainMenuScreen(GUIScreen):
    def __init__(self, stage):
        GUIScreen.__init__(self, stage)

        #scale = (360,40)

        #Botón de inicio de juego
        self.gameStart = GUIButton(self, MENU_START_BUTTON_UP_LOCATION, MENU_START_BUTTON_DOWN_LOCATION, getattr(self, 'button_fun_start'), (0,0))
        self.gameStart.set_position((SCREEN_WIDTH/2, SCREEN_HEIGHT/2-30), 'center')
        #Botón para salir del juego
        self.gameExit = GUIButton(self, MENU_EXIT_BUTTON_UP_LOCATION, MENU_EXIT_BUTTON_DOWN_LOCATION, getattr(self, 'button_fun_exit'), (0,0))
        self.gameExit.set_position((SCREEN_WIDTH/2, SCREEN_HEIGHT/2+30), 'center')

        self.add_element(self.gameStart)
        self.add_element(self.gameExit)

        self.elementClick = None

        # Elementos del fondo
        self.background = ResourceManager.load_image('interface/mainscreen/background.png')
        self.bonefire = MyStaticAnimatedSprite('mainmenu/bonefire.png', 'mainmenu/bonefire.json')
        self.light = ResourceManager.load_image('interface/mainscreen/light.png', -1)
        self.player = ResourceManager.load_image('interface/mainscreen/player.png')
        self.shadow = ResourceManager.load_image('interface/mainscreen/shadow.png', -1)

    def events(self, event_list):
        for event in event_list:
            if event.type == MOUSEBUTTONDOWN:
                self.elementClick = None
                for element in self.GUIElements:
                    if element.__class__.__name__ == 'GUIButton' and element.position_is_in_element((event.pos[0]/SCALE_FACTOR, event.pos[1]/SCALE_FACTOR)):
                        element.action()
                        self.elementClick = element
            if event.type == MOUSEBUTTONUP:
                for element in self.GUIElements:
                    if element.__class__.__name__ == 'GUIButton':
                        if element.position_is_in_element((event.pos[0]/SCALE_FACTOR, event.pos[1]/SCALE_FACTOR)):
                            if (element == self.elementClick):
                                element.action()
                                #self.stage.remove_window_dialog()
                        elif(element == self.elementClick):
                            element.swap()

    def button_fun_start(self):
        self.stage.gameManager.scene_change(self.stage.startStage)

    def button_fun_exit(self):
        self.stage.gameManager.program_exit()

    def update(self, time):
        # Actualizamos la hoguera
        self.bonefire.update(time)
        # Actualiamos la Interfaz
        GUIScreen.update(self, time)

    def draw(self, screen):
        # Mostamos el fondo
        screen.blit(self.background, (0,0))
        screen.blit(self.bonefire.image, (46, 212))
        screen.blit(self.player, (39, 241))
        screen.blit(self.light, (23, 209))
        screen.blit(self.shadow, (19, 273))
        # Mostramos la interfaz
        GUIScreen.draw(self, screen)
