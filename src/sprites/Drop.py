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

        # Obtenemos el nombre de la carpeta del sprite sheet y del archivo de configuración
        fullname = os.path.join('items', spriteName)
        imagePath = os.path.join('sprites', fullname + '.png')

        # Cargar sheet de sprites
        self.sheet = ResourceManager.load_image(imagePath, -1)

        # Leer coordenadas de fichero
        data = ResourceManager.load_sprite_conf(fullname + '.json')
        self.sheetConf = []

        # Cargamos los sprites
        for col in range(0, len(data)):
            cell = data[col]
            coords = pygame.Rect((int(cell['x']), int(cell['y'])), (int(cell['width']), int(cell['height'])))
            delay = float(cell['delay'])*1000
            self.sheetConf.append({'coords': coords, 'delay': delay})

        # Animación inicial
        self.animationFrame = 0
        self.currentDelay = 0

        self.rect = pygame.Rect(0, 0, self.sheetConf[0]['coords'][2], self.sheetConf[0]['coords'][3])

        # Frame inicial
        self.image = self.sheet.subsurface(self.sheetConf[0]['coords'])

        # Cantidad de elementos del Drop
        self.amount = amount

    def update(self, time):
        # Actualizamos el retardo
        self.currentDelay -= time

        # Miramos si ha pasado el retardo para dibujar una nueva postura
        if self.currentDelay < 0:
            # Actualizamos el delay
            self.currentDelay = self.sheetConf[self.animationFrame]['delay']
            # Actualizamos la postura
            self.animationFrame += 1

            # Reiniciamos la animación si nos hemos pasado de frames
            if self.animationFrame >= len(self.sheetConf):
                self.animationFrame = 0

            # Actualiamos la imagen con el frame correspondiente
            self.image = self.sheet.subsurface(self.sheetConf[self.animationFrame]['coords'])

            self.rect.width = self.image.get_width()
            self.rect.height = self.image.get_height()

            self.mask = pygame.mask.from_surface(self.image)
