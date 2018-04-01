# -*- coding: utf-8 -*-

from src.scenes.stage.StageState import *
from src.interface.screens.GUICreditsScreen import *

class OnCreditsState(StageState):
    def __init__(self, stage):
        stage.guiCredits = GUICreditsScreen(self, stage)

    def update(self, time, stage):
        pass

    def events(self, events, stage):
        pass

    def draw(self, screen):
        pass
