# -*- coding: utf-8 -*-

import pygame
from src.sprites.MyStaticSprite import *
from src.sprites.Collectable import *
from src.ResourceManager import *

SPRITES_PATH = os.path.join('keys')

class Key(MyStaticSprite, Collectable):
    def __init__(self, position, imageFile):
        # Llamamos a los constructores
        MyStaticSprite.__init__(self)
        Collectable.__init__(self)
        # Cargamos la imagen de la llave
        self.image = ResourceManager.load_image(os.path.join(SPRITES_PATH, imageFile), -1)
        self.rect = self.image.get_rect()
        # Posicionamos el elemento
        self.change_position(position)

    def collect(self, stage):
        stage.player.inventary.append(self)
        self.kill()
