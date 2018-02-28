#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importar modulos
import pygame
import GameManager
from GameManager import *
from MainMenu import Menu

if __name__ == '__main__':
    # Inicializamos la libreria de pygame
    pygame.init()
    # Creamos el director
    gameManager = GameManager()
    # Creamos la escena con la pantalla inicial
    scene = Menu(gameManager)
    # Le decimos al director que apile esta escena
    gameManager.scene_stack(scene)
    # Y ejecutamos el juego
    gameManager.run()
    # Cuando se termine la ejecución, finaliza la librería
    pygame.quit()
