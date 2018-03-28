# -*- coding: utf-8 -*-

import pygame
from src.scenes.stage.StageState import *
from src.scenes.Scene import *

class OnLeaveState(StageState):
    def __init__(self):
        StageState.__init__(self)
        self.alpha = 0
        self.black = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

    def update(self, time, stage):
        self.alpha = min(self.alpha + time*0.128, 255)

        if self.alpha == 255 and not self.finishAnimation:
            stage.player.move(STILL)
            nextStage = Stage(stage.stageNum+1, stage.gameManager, stage.player)
            stage.gameManager.scene_change(nextStage)
            return

    def events(self, events, stage):
        pass

    def draw(self, screen, stage):
        StageState.draw(self, screen, stage)
        self.black.set_alpha(int(self.alpha))
        screen.blit(self.black, (0, 0))
