# -*- coding: utf-8 -*-

import pygame
from src.ResourceManager import *
from src.sprites.MyStaticSprite import *

class ShieldSprite(MyStaticSprite):
    def __init__(self, imageFile, spriteSheet):
        # Primero invocamos al constructor de la clase padre
        MyStaticSprite.__init__(self)

        self.shieldSheet = ResourceManager.load_image(os.path.join('sprites', imageFile), (-1))

        # Leer coordenadas de fichero
        data = ResourceManager.load_sprite_conf(spriteSheet)
        sheetConf = []

        # Cargamos el sprite del escudo
        for col in range(0, len(data)):
            cell = data[col]
            coords = pygame.Rect((int(cell['x']), int(cell['y'])), (int(cell['width']), int(cell['height'])))
            delay = float(cell['delay'])*1000
            sheetConf.append({'coords': coords, 'delay': delay})

        # El rectangulo del Sprite
        self.rect = pygame.Rect(0, 0, sheetConf[0]['coords'][2], sheetConf[0]['coords'][3])

        # Imagen
        self.image = self.shieldSheet.subsurface(sheetConf[0]['coords'])