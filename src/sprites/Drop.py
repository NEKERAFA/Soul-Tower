# -*- coding: utf-8 -*-

import pygame, os
from src.ResourceManager import *
from src.sprites.MySprite import *

# -------------------------------------------------
# Clase Drop

class Drop(MySprite):
    def __init__(self, spriteName, amount):
        # Primero invocamos al constructor de la clase padre
        MySprite.__init__(self)
        # Obtenemos el nombre del item
        fullname = os.path.join('sprites', 'items', spriteName + '.png')
        # Cargamos la imagen
        self.image = ResourceManager.load_image(fullname, -1)
        # Rectángulo
        self.rect = self.image.get_rect()
        # Cantidad de elementos del Drop
        self.amount = amount
