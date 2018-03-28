# -*- coding: utf-8 -*-

import pygame
from src.scenes.stage.StageState import *
from src.scenes.stage.OnDialogueState import *

class OnMagicWindowState(StageState):
    def __init__(self, magicWindow, stage):
        self.previousState = stage.state
        self.magicWindow = magicWindow
        self.initialDialog = False
        self.setSelection = False
        self.endDialog = False

    def update(self, time, stage):
        if not self.initialDialog:
            # Lanzamos el diálogo principal
            self.initialDialog = True
            # TODO
            stage.state = OnDialogueState('test.json', stage)
        elif not self.setSelection:
            # Lanzamos la selección
            print 'Aquí está la intervención'
            # TODO
            self.setSelection = True
        elif not self.endDialog:
            # Lanzamos el diálogo principal
            self.endDialog = True
            # TODO
            stage.state = OnDialogueState('test.json', stage)
        else:
            self.magicWindow.destruct(stage)
            stage.state = self.previousState

    def events(self, events, stage):
        pass
