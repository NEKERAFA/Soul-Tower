# -*- coding: utf-8 -*-

import pygame
from src.scenes.stage.StageState import *
from src.scenes.Scene import *

class OnEnterState(StageState):
    def __init__(self):
        StageState.__init__(self)
        self.finishAnimation = False
        self.alpha = 255
        self.black = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

    def update(self, time, stage):
        self.alpha = max(self.alpha - time*0.256, 0)

        if self.alpha == 0 and not self.finishAnimation:
            self.finishAnimation = True

        # Player
        currentRoom = stage.rooms[stage.currentRoom]
        # Actualizamos los sprites
        # Player
        stage.player.update(time, currentRoom.rect, stage.mask)
        # Enemigos
        currentRoom.enemies.update(time, currentRoom.rect, stage.mask)

    def events(self, events, stage):
        pass

    def draw(self, screen, stage):
        StageState.draw(self, screen, stage)
        self.black.set_alpha(int(self.alpha))
        screen.blit(self.black, (0, 0))
