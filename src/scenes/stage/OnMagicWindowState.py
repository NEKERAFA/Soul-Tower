# -*- coding: utf-8 -*-

import pygame
from src.scenes.stage.StageState import *
from src.scenes.stage.OnDialogueState import *
from src.interface.screens.GUIWindowDialogScreen import *

class OnMagicWindowState(StageState):
    def __init__(self, magicWindow, stage):
        self.previousState = stage.state
        self.magicWindow = magicWindow
        self.initialDialog = False
        self.setSelection = False
        self.endDialog = False
        self.guiWindow = None

    def update(self, time, stage):
        if not self.initialDialog:
            # Lanzamos el diálogo principal
            self.initialDialog = True
            stage.state = OnDialogueState(self.magicWindow.initialDialog, stage)
        elif not self.setSelection:
            # Lanzamos la selección
            #print 'Aquí está la intervención'
            # TODO
            if(self.guiWindow is None):
                self.guiWindow = stage.create_window_dialog(self.magicWindow.selectionFile)
            if(self.guiWindow.choice >= 0):
                self.setSelection = True
        elif not self.endDialog:
            self.endDialog = True
            stage.remove_window_dialog()
            stage.state = OnDialogueState(self.magicWindow.endDialogs[self.guiWindow.choice], stage)
        else:
            self.magicWindow.destruct(stage)
            stage.state = self.previousState

        if(self.guiWindow is not None):
            self.guiWindow.update(time)

    def events(self, events, stage):
        if(stage.guiWindow is not None):
            stage.guiWindow.events(events)
