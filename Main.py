#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importar modulosa
import pygame, random
from datetime import datetime
from src.GameManager import *
from src.scenes.InitialStage import *

if __name__ == '__main__':
    # Iniciamos la semilla
    random.seed(datetime.now())
    # Se prepara el mixer e inicializamos la libreria de pygame
    pygame.mixer.pre_init(44100, 16, 2, 4096)
    pygame.init()
    #pygame.mixer.init()
    # Creamos el director
    # global gameManager
    gameManager = GameManager()
    # Creamos la escena con la pantalla inicial
    scene = Stage(1, gameManager)
    # Le decimos al director que apile esta escena
    gameManager.scene_stack(scene)
    # Y ejecutamos el juegow
    print (pygame.mixer.get_num_channels())
    gameManager.run()
    # Cuando se termine la ejecución, finaliza la librería
    pygame.quit()
