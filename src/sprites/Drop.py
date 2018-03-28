# -*- coding: utf-8 -*-

import pygame, os
from src.ResourceManager import *
from src.sprites.MyStaticAnimatedSprite import *

DROP_PATH = 'drops'

# -------------------------------------------------
# Clase Drop

class Drop(MyStaticAnimatedSprite):
    def __init__(self, spriteName, amount):
        # Nombre del drop
        self.name = spriteName

        # Obtenemos el nombre de la carpeta del sprite sheet y del archivo de configuración
        fullname = os.path.join(DROP_PATH, spriteName)

        # Primero invocamos al constructor de la clase padre
        MyStaticAnimatedSprite.__init__(self, fullname + '.png', fullname + '.json')

        # Cantidad de elementos del Drop
        self.amount = amount
