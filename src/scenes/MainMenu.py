# -*- encoding: utf-8 -*-

import pygame, pyganim

from pygame.locals import *
from src.scenes.Scene import *
from src.ResourceManager import *

# -------------------------------------------------
# Clase Menu, la escena en sí

class MainMenu(Scene):
    def __init__(self, gameManager):
        # Llamamos al constructor de la clase padre
        Scene.__init__(self, gameManager);
        # Creamos la lista de pantallas
        self.screenList = []
        # Creamos las pantallas que vamos a tener
        #   y las metemos en la lista
        self.screenList.append(GUIStartScreen(self))
        # En que pantalla estamos actualmente
        self.show_start_screen()

    def update(self, *args):
        return

    def events(self, event_list):
        # Se mira si se quiere salir de esta escena
        for event in event_list:
            # Si se quiere salir, se le indica al director
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.programExit()
            elif event.type == pygame.QUIT:
                self.gameManager.programExit()

        # Se pasa la lista de eventos a la pantalla actual
        self.screenList[self.currentScreen].events(event)

    def draw(self, pantalla):
        self.listaPantallas[self.pantallaActual].dibujar(pantalla)

    #--------------------------------------
    # Metodos propios del menu

    def program_exit(self):
        self.gameManager.program_exit()

    #def runGame(self):
    #    stage = Stage(self.director)
    #    self.gameManager.sceneStack(stage)

    def show_start_screen(self):
        self.startScreen = 0

    # def mostrarPantallaConfiguracion(self):
    #    self.pantallaActual = ...
