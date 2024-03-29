# -*- coding: utf-8 -*-

import pygame, os
import math as m
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
WINDOW_WARRIOR_LOCATION = os.path.join('interface', 'game', 'button_sword.png')
WINDOW_SORCERESS_LOCATION = os.path.join('interface', 'game', 'button_staff.png')
WINDOW_BOTH_LOCATION = os.path.join('interface', 'game', 'button_both.png')

class GUIWindowDialogScreen(GUIScreen):
    def __init__(self, stage, selectionFile):
        GUIScreen.__init__(self, stage)
        #self.selectionFile = ["Texto 1", "Texto 2", "Texto 3", "Texto 4", "Texto 5", "Texto 6", "Texto 7", "Texto 8", "Texto 9"]
        self.selectionFile = ResourceManager.load_dialogue(selectionFile)
        self.choice = -1
        self.elementClick = None
        iniVal = 3*(self.stage.stageNum-1)
        finVal = iniVal+3

        scale = (360,40)

        initPosition = (int((SCREEN_WIDTH-scale[0])/2), int(SCREEN_HEIGHT/2)-scale[1]*1.5)

        choiceSymbolsLocations = [WINDOW_SORCERESS_LOCATION, WINDOW_WARRIOR_LOCATION, WINDOW_BOTH_LOCATION]

        if(self.stage.player.choseAnythingNotShared):
            finVal -= 1

        for i in range(iniVal,finVal):
            text = self.selectionFile[i]
            nextPosition = (initPosition[0], initPosition[1]+(i%3)*(scale[1]+10)+40)
            button = GUIWindowButton(text, WINDOW_BUTTON_UP_LOCATION, WINDOW_BUTTON_DOWN_LOCATION, choiceSymbolsLocations[(i%3)], getattr(self, 'button_fun_'+str(i)), nextPosition, scale)
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
                                if(self.choice is not 2):
                                    self.stage.player.choseAnythingNotShared = True
                                #self.stage.remove_window_dialog()
                        elif(element == self.elementClick):
                            element.swap()

    def button_fun_0(self):
        self.choice = 0
        self.stage.player.choiceAdder += 1
        self.stage.player.add_max_energy()
        self.stage.player.add_max_energy()

    def button_fun_1(self):
        self.choice = 1
        self.stage.player.choiceAdder -= 1
        self.stage.player.add_max_life()
        self.stage.player.add_max_life()

    def button_fun_2(self):
        self.choice = 2
        self.stage.player.add_max_life()
        self.stage.player.add_max_energy()

    def button_fun_3(self):
        self.choice = 0
        self.stage.player.choiceAdder += 1
        self.stage.player.add_max_energy()
        self.stage.player.stats["rng_del"] = 100

    def button_fun_4(self):
        self.choice = 1
        self.stage.player.choiceAdder -= 1
        self.stage.player.killedFriend = True
        self.stage.player.add_max_life()
        self.stage.player.stats["mel_del"] = 200

    def button_fun_5(self):
        self.choice = 2
        self.stage.player.stats["nrg_reg"] = 0.002
        self.stage.player.stats["nrg_reg_bck"] = 0.001

    def button_fun_6(self):
        self.choice = 0
        self.stage.player.choiceAdder += 1
        self.stage.player.add_max_energy()
        self.stage.player.stats["atk"] = 2


    def button_fun_7(self):
        self.choice = 1
        self.stage.player.choiceAdder -= 1
        self.stage.player.add_max_life()
        self.stage.player.stats["spd"] = 0.3
        self.stage.player.diagonalSpeed = m.sqrt((self.stage.player.stats["spd"] * self.stage.player.stats["spd"])/2.0)

    def button_fun_8(self):
        self.choice = 2
        self.stage.player.add_max_life()
        self.stage.player.add_max_energy()
        self.stage.player.stats["atk"] = 2
        self.stage.player.stats["spd"] = 0.3
        self.stage.player.diagonalSpeed = m.sqrt((self.stage.player.stats["spd"] * self.stage.player.stats["spd"])/2.0)
