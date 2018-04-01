# -*- coding: utf-8 -*-

import pygame

from src.scenes.Scene import *
from src.scenes.InitialStage import *
from src.interface.screens.GUIMainMenuScreen import *
from src.ResourceManager import *

class MainMenuScene(Scene):
    #TODO añadir fondo
    def __init__(self, gameManager):
        Scene.__init__(self, gameManager)

        # Se le pasa la escena actual como "stage" aunque técnicamente no sea una fase
        self.guiMenu = GUIMainMenuScreen(self)

        # Primera fase
        self.startStage = InitialStage(gameManager)

<<<<<<< HEAD
        # Música de la pantalla inicial
        ResourceManager.load_music('Menu_principal.ogg')
        pygame.mixer.music.play(-1, 0.0)
=======
    def new_menu(self, gameManager):
        return MainMenuScene(gameManager)
>>>>>>> 377f47b11653a858a3c434bb7267ee969feecba2

    def update(self, time):
        self.guiMenu.update(time)

    def events(self, events):
        for event in events:
            # Si se quiere salir, se le indica al director
            if event.type == pygame.QUIT:
                self.gameManager.program_exit()
                return
        self.guiMenu.events(events)

    def draw(self, screen):
        self.guiMenu.draw(screen)
