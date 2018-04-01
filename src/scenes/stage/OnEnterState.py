# -*- coding: utf-8 -*-

import pygame
from src.scenes.stage.StageState import *
from src.scenes.Scene import *

class OnEnterState(StageState):
    def __init__(self):
        StageState.__init__(self)
        self.alpha = 255
        self.black = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

    def update(self, time, stage):
        self.alpha = max(self.alpha - time*0.256, 0)

        if self.alpha == 0:
            if stage.rooms[stage.currentRoom].small:
                stage.set_state(stage.smallRoomState)
            else:
                stage.set_state(stage.inRoomState)
            stage.state.update(time, stage)
            return

        # Player
        currentRoom = stage.rooms[stage.currentRoom]
        # Actualizamos los sprites
        # Player
        stage.player.update(time, stage)
        # Enemigos
        currentRoom.enemies.update(time, currentRoom.rect, stage)

        # Actualizamos la interfaz
        stage.gui.update(time)

    def events(self, events, stage):
        stage.gui.events(events)

    def draw(self, screen, stage):
        StageState.draw(self, screen, stage)
        self.black.set_alpha(int(self.alpha))
        screen.blit(self.black, (0, 0))
