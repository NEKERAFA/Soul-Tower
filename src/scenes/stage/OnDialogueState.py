# -*- coding: utf-8 -*-

import pygame
from src.scenes.Stage import *
from src.scenes.stage.StageState import *
from src.interface.GUIDialog import *

class OnDialogueState(StageState):
    # Recibe un trigger y la stage (de la que se saca el estado anterior y la GUI), lanza un diálogo (init)
    def __init__(self, dialogue, stage, isFile=True):
        self.previousState = stage.state
        if isFile:
            self.dialogue = ResourceManager.load_dialogue(dialogue)
        else:
            self.dialogue = dialogue
        self.spacePressed = False
        self.intervention = 0

        # TODO añadir caja de diálogo a la pantalla GUI
        self.dialogueBox = GUIDialog(self.dialogue[0])
        stage.gui.add_element(self.dialogueBox)

    # TODO modo automático con otra tecla
    def update(self, time, stage):
        stage.gui.update(time)

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
                    stage.gui.remove_element(self.dialogueBox)
                    self.dialogueBox = GUIDialog(self.dialogue[self.intervention])
                    stage.gui.add_element(self.dialogueBox)
                # Terminamos el diálogo
                else:
                    stage.set_state(self.previousState)
                    stage.gui.remove_element(self.dialogueBox)
