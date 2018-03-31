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
    pygame.mixer.pre_init(44100, 16, 2, 4096)
    pygame.mixer.init()
    #pygame.mixer.set_num_channels(40)
    # Creamos el director
    # global gameManager
    gameManager = GameManager()
    # Creamos la escena con la pantalla inicial
    scene = Stage(1, gameManager)
    scene.player.killedFriend = False
    #scene = MainMenuScene(gameManager)
    # Le decimos al director que apile esta escena
    gameManager.scene_stack(scene)
    # Y ejecutamos el juego
    print (pygame.mixer.get_num_channels())
    gameManager.run()
    # Cuando se termine la ejecución, finaliza la librería
    pygame.quit()
