# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
from src.ResourceManager import *
from src.scenes.Scene import *
from src.interface.screens.GUIScreen import *
from src.interface.GUIButton import *

# -------------------------------------------------
# Clase GUIMenuScreen
# Interfaz durante los menús

# Localización de los sprites
WINDOW_BUTTON_UP_LOCATION = 'interface/player/button_up_placeholder.png'
WINDOW_BUTTON_DOWN_LOCATION = 'interface/player/button_down_placeholder.png'

class GUIWindowDialogScreen(GUIScreen):
    def __init__(self, stage):
        GUIScreen.__init__(self, stage)

        iniVal = 1+2*(self.stage.stageNum-1)
        finVal = iniVal+3

        scale = (100,40)

        initPosition = (int((SCREEN_WIDTH-scale[0])/2), int(SCREEN_HEIGHT/2)-scale[1])

        for i in range(iniVal,finVal):
            button = GUIButton(self, WINDOW_BUTTON_UP_LOCATION, WINDOW_BUTTON_DOWN_LOCATION, (initPosition[0], initPosition[1]+i*40), scale, getattr(self, 'button_fun_'+str(i)))
            self.add_element(button)

    def events(self, event_list):
        for event in event_list:
            if event.type == MOUSEBUTTONDOWN:
                self.elementClick = None
                for element in self.GUIElements:
                    if element.__class__.__name__ == 'GUIButton' and element.position_is_in_element((event.pos[0]/SCALE_FACTOR, event.pos[1]/SCALE_FACTOR)):
                        self.elementClick = element
                        element.action()
            if event.type == MOUSEBUTTONUP:
                for element in self.GUIElements:
                    if element.__class__.__name__ == 'GUIButton':
                        if element.position_is_in_element((event.pos[0]/SCALE_FACTOR, event.pos[1]/SCALE_FACTOR)):
                            if (element == self.elementClick):
                                element.action()
                                self.stage.remove_window_dialog()
                        elif(element == self.elementClick):
                            element.swap()

    def button_fun_1(self):
        print("function 1")

    def button_fun_2(self):
        print("function 2")

    def button_fun_3(self):
        print("function 3")

    def button_fun_4(self):
        print("function 4")

    def button_fun_5(self):
        print("function 5")

    def button_fun_6(self):
        print("function 6")

    def button_fun_7(self):
        print("function 7")

    def button_fun_8(self):
        print("function 8")

    def button_fun_9(self):
        print("function 9")
