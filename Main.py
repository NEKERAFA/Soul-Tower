#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importar modulos
import pygame
import GameManager
from GameManager import *
from InitialStage import *

if __name__ == '__main__':
    # Inicializamos la libreria de pygame
    pygame.init()
    # Creamos el director
    gameManager = GameManager()
    # Creamos la escena con la pantalla inicial
    scene = InitialStage(gameManager)
    # Le decimos al director que apile esta escena
    gameManager.scene_stack(scene)
    # Y ejecutamos el juego
    gameManager.run()
    # Cuando se termine la ejecución, finaliza la librería
    pygame.quit()
