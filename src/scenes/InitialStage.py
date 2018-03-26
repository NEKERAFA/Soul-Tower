# -*- coding: utf-8 -*-

import pygame
from src.scenes.Stage import *
from src.interface.screens.GUITutorialScreen import *

# -------------------------------------------------
# Clase InitialState

class InitialStage(Stage):
    def __init__(self, gameManager):
        # Primero invocamos al constructor de la clase padre
        Stage.__init__(self, 1, gameManager)
        # Cargamos la interfaz del tutorial
        self.guiTutorial = GUITutorialScreen()

    def update(self, time):
        # Delegamos en la superclase
        Stage.update(self, time)
        # Actualizamos lo que haya que actualizar del tutorial
        self.guiTutorial.update(time)

    def events(self, events):
        # Delegamos en la superclase
        Stage.events(self, events)
        # Actualizamos lo que haya que actualizar del tutorial
        self.guiTutorial.events(events)

    def draw(self, screen):
        # Delegamos en la superclase
        Stage.draw(self, screen)
        # Mostramos la pantalla del tutorial
        self.guiTutorial.draw(screen)
