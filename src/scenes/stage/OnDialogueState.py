# -*- coding: utf-8 -*-

import pygame
from src.scenes.Stage import *
from src.scenes.stage.State import *
from src.interface.GUIDialog import *

class OnDialogueState(State):
    # Recibe un trigger y la stage (de la que se saca el estado anterior y la GUI), lanza un diálogo (init)
    def __init__(self, dialogue, stage):
        self.previousState = stage.state
        self.dialogue = ResourceManager.load_dialogue(dialogue)
        self.spacePressed = False
        self.intervention = 0

        # TODO añadir caja de diálogo a la pantalla GUI
        self.dialogueBox = GUIDialog(stage.gui, "interface/game/dialog_placeholder.png", (DIALOG_LEFT, DIALOG_BOTTOM), (DIALOG_WIDTH, DIALOG_HEIGHT), pygame.font.SysFont('dejavusans', 14), self.dialogue[0], 0.04)
        stage.gui.addElement(self.dialogueBox)

    # TODO modo automático con otra tecla
    def update(self, time, stage):
        pass

    def events(self, events, stage):
        # Responder a pulsaciones del teclado.
        # Avanza el texto. Cuando no quede texto, elimina el diálogo y vuelve al estado anterior
        for event in events:
            if event.type == KEYDOWN and event.key == K_SPACE:
                self.spacePressed = True
            elif event.type == KEYUP and event.key == K_SPACE and self.spacePressed:
                # Avanzamos el diálogo
                if not self.dialogueBox.is_finished():
                    self.dialogueBox.next()
                # Pasamos a la siguiente intervención
                elif self.intervention < len(self.dialogue) - 1:
                    self.intervention += 1
                    stage.gui.removeElement(self.dialogueBox)
                    self.dialogueBox = GUIDialog(stage.gui, "interface/game/dialog_placeholder.png", (DIALOG_LEFT, DIALOG_BOTTOM), (DIALOG_WIDTH, DIALOG_HEIGHT), pygame.font.SysFont('dejavusans', 14), self.dialogue[self.intervention], 0.04)
                    stage.gui.addElement(self.dialogueBox)
                # Terminamos el diálogo
                else:
                    stage.state = self.previousState
                    stage.gui.removeElement(self.dialogueBox)
