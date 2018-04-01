#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importar modulos
import pygame, random
from datetime import datetime
from src.GameManager import *
from src.scenes.MainMenuScene import *

if __name__ == '__main__':
    # Iniciamos la semilla
    random.seed(datetime.now())
    # Inicializamos la libreria de pygame y el mixera
    pygame.init()
    # Creamos el director
    # global gameManager
    gameManager = GameManager()
    # Creamos la escena con la pantalla inicial
    scene = Stage(3, gameManager)
    #scene = MainMenuScene(gameManager)
    # Le decimos al director que apile esta escena
    gameManager.scene_stack(scene)
    # Y ejecutamos el juego
    gameManager.run()
    # Cuando se termine la ejecución, finaliza la librería
    pygame.quit()
