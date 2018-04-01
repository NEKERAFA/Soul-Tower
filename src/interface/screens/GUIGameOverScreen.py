# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
from src.ResourceManager import *
from src.scenes.Stage import *
from src.interface.screens.GUIScreen import *
from src.interface.GUIImage import *
from src.interface.GUIButton import *


# -------------------------------------------------
# Clase GUIGameOverScreen
# Pantalla que aparece al morir

# Localización de los sprites
GAME_OVER_TEXT_LOCATION = os.path.join(INTERFACE_GAME_FOLDER, 'gui_game_over_text.png')
DEAD_CHARACTER_SPRITE_LOCATION = os.path.join(INTERFACE_GAME_FOLDER, 'gui_dead_character_sprite.png')
MENU_CONTINUE_BUTTON_UP_LOCATION = os.path.join(INTERFACE_GAME_FOLDER, 'continue_up.png')
MENU_CONTINUE_BUTTON_DOWN_LOCATION = os.path.join(INTERFACE_GAME_FOLDER, 'continue_down.png')
MENU_EXIT_BUTTON_UP_LOCATION = os.path.join(INTERFACE_GAME_FOLDER, 'exit_up.png')
MENU_EXIT_BUTTON_DOWN_LOCATION = os.path.join(INTERFACE_GAME_FOLDER, 'exit_down.png')

class GUIGameOverScreen(GUIScreen):
    def __init__(self, stage):
        GUIScreen.__init__(self, stage)
        # Texto de muerte
        self.gameOverText = GUIImage(self, GAME_OVER_TEXT_LOCATION, (0,SCREEN_HEIGHT/2-50))

        # Botones para continuar / salir
        self.continueButton = GUIButton(self, MENU_CONTINUE_BUTTON_UP_LOCATION, MENU_CONTINUE_BUTTON_DOWN_LOCATION, getattr(self, 'button_fun_continue'), (0,0))
        self.continueButton.set_position((SCREEN_WIDTH/2, SCREEN_HEIGHT/2+25), 'center')
        self.gameExit = GUIButton(self, MENU_EXIT_BUTTON_UP_LOCATION, MENU_EXIT_BUTTON_DOWN_LOCATION, getattr(self, 'button_fun_exit'), (0,0))
        self.gameExit.set_position((SCREEN_WIDTH/2, SCREEN_HEIGHT/2+75), 'center')

        # Sprite del personaje muerto
        self.deadCharacter = GUIImage(self, DEAD_CHARACTER_SPRITE_LOCATION, (SCREEN_WIDTH/2-20, SCREEN_HEIGHT-35))

        # Surface para hacer un fadeout
        self.alpha = 0
        self.black = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

        self.add_element(self.gameOverText)
        self.add_element(self.continueButton)
        self.add_element(self.gameExit)
        self.add_element(self.deadCharacter)

    def update(self, time):
        GUIScreen.update(self, time)
        self.alpha = min(self.alpha + time*0.1, 255)

    def draw(self, screen):
        self.black.set_alpha(int(self.alpha))
        screen.blit(self.black, (0, 0))
        GUIScreen.draw(self, screen)

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
                        elif(element == self.elementClick):
                            element.swap()

    def button_fun_exit(self):
        self.stage.gameManager.program_exit()

    def button_fun_continue(self):
        #scene = Stage(self.stage.stageNum, gameManager, None, self.stage.savedData)
        scene = self.stage.new_stage(self.stage.savedData)
        self.stage.gameManager.scene_change(scene)
