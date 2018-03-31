# -*- coding: utf-8 -*-

import pygame
from src.sprites.MyStaticSprite import *
from src.sprites.Interactive import *
from src.ResourceManager import *

class Upgrade(MyStaticSprite, Interactive):
    def __init__(self, position, imageFile, cost, upgrade):
        # Llamamos al constructor de la clase
        MyStaticSprite.__init__(self)
        # Cambiamos la posición del sprite
        self.change_position(position)
        # Obtenemos la imagen
        self.image = ResourceManager.load_image(imageFile, -1)
        Interactive.__init__(self, self.rect)
        self.cost = cost
        self.upgrade = upgrade

    def activate(self, stage):
        if stage.player.souls >= self.cost:
            stage.player.decrement_souls(self.cost)
            if self.upgrade == 'ranged':
                stage.player.rangedLevel += 1
            elif self.upgrade == 'melee':
                stage.player.meleeLevel += 1
