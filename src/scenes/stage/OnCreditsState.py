# -*- coding: utf-8 -*-

from src.scenes.stage.StageState import *
from src.interface.screens.GUICreditsScreen import *

class OnCreditsState(StageState):
    def __init__(self, stage):
        stage.guiCredits = GUICreditsScreen(stage)

    def update(self, time, stage):
        if stage.guiCredits is not None:
            stage.guiCredits.update(time)

    def events(self, events, stage):
        pass

    def draw(self, screen, stage):
        if(stage.guiCredits is not None):
            stage.guiCredits.draw(screen)
