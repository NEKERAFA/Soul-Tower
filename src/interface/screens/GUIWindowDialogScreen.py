# -*- coding: utf-8 -*-

import pygame, os
from pygame.locals import *
from src.ResourceManager import *
from src.scenes.Scene import *
from src.interface.screens.GUIScreen import *
from src.interface.GUIWindowButton import *

# -------------------------------------------------
# Clase GUIMenuScreen
# Interfaz durante los menús

# Localización de los sprites
WINDOW_BUTTON_UP_LOCATION = os.path.join('interface', 'game', 'button_up.png')
WINDOW_BUTTON_DOWN_LOCATION = os.path.join('interface', 'game', 'button_down.png')

class GUIWindowDialogScreen(GUIScreen):
    def __init__(self, stage, selectionFile):
        GUIScreen.__init__(self, stage)
        self.selectionFile = ResourceManager.load_dialogue(selectionFile)
        self.choice = -1
        self.elementClick = None
        iniVal = 1+2*(self.stage.stageNum-1)
        finVal = iniVal+3

        scale = (360,40)

        initPosition = (int((SCREEN_WIDTH-scale[0])/2), int(SCREEN_HEIGHT/2)-scale[1]*1.5)

        for i in range(iniVal,finVal):
            text = self.selectionFile[i-1]
            button = GUIWindowButton(self, text, WINDOW_BUTTON_UP_LOCATION, WINDOW_BUTTON_DOWN_LOCATION, (initPosition[0], initPosition[1]+i*(scale[1]+10)), scale, getattr(self, 'button_fun_'+str(i)))
            self.add_element(button)

    def events(self, event_list):
        for event in event_list:
            if event.type == MOUSEBUTTONDOWN:
                self.elementClick = None
                for element in self.GUIElements:
                    if element.__class__.__name__ == 'GUIWindowButton' and element.position_is_in_element((event.pos[0]/SCALE_FACTOR, event.pos[1]/SCALE_FACTOR)):
                        element.action()
                        self.elementClick = element
            if event.type == MOUSEBUTTONUP:
                for element in self.GUIElements:
                    if element.__class__.__name__ == 'GUIWindowButton':
                        if element.position_is_in_element((event.pos[0]/SCALE_FACTOR, event.pos[1]/SCALE_FACTOR)):
                            if (element == self.elementClick):
                                element.action()
                                #self.stage.remove_window_dialog()
                        elif(element == self.elementClick):
                            element.swap()

    def button_fun_1(self):
        self.choice = 0

    def button_fun_2(self):
        self.choice = 1

    def button_fun_3(self):
        self.choice = 2

    def button_fun_4(self):
        self.choice = 0

    def button_fun_5(self):
        self.choice = 1

    def button_fun_6(self):
        self.choice = 2

    def button_fun_7(self):
        self.choice = 0

    def button_fun_8(self):
        self.choice = 1

    def button_fun_9(self):
        self.choice = 3
