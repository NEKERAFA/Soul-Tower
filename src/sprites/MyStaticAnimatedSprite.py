# -*- coding: utf-8 -*-

import pygame, os
from src.ResourceManager import *
from src.sprites.MyStaticSprite import *

SPRITES_PATH = 'sprites'

# Sprites estáticos
class MyStaticAnimatedSprite(MyStaticSprite):
    def __init__(self, imageFile, spriteSheet):
        # Primero invocamos al constructor de la clase padre
        MyStaticSprite.__init__(self)

        # Cargar sheet de sprites
        self.sheet = ResourceManager.load_image(os.path.join(SPRITES_PATH, imageFile), -1)

        # Leer el fichero de configuración
        data = ResourceManager.load_sprite_conf(spriteSheet)

        # Cargamos los sprites
        self.sheetConf = []
        for row in range(0, len(data)):
            self.sheetConf.append([])
            tmp = self.sheetConf[row]
            for cell in data[row]:
                # Creamos las coordenadas
                coords = pygame.Rect((int(cell['x']), int(cell['y'])), (int(cell['width']), int(cell['height'])))
                # Cargamos el delay y lo convertimos en milisegundos
                delay = float(cell['delay'])*1000
                # Guardamos la configuración
                tmp.append({'coords': coords, 'delay': delay})

        # Animación inicial
        self.animationNum = 0
        self.animationFrame = 0

        # El rectangulo del Sprite
        self.rect = pygame.Rect(0, 0, self.sheetConf[0][0]['coords'][2], self.sheetConf[0][0]['coords'][3])

        # Frame inicial
        self.image = self.sheet.subsurface(self.sheetConf[0][0]['coords'])

        # Delay actual
        self.currentDelay = self.sheetConf[0][0]['delay']

        # Máscara de la animación
        self.mask = pygame.mask.from_surface(self.image)

        # Hace loop de la animación
        self.animationLoop = True
        self.animationFinish = False

    def update(self, time):
        if not self.animationFinish:
            # Actualizamos el retardo
            self.currentDelay -= time
            currentAnim = self.sheetConf[self.animationNum]

            # Miramos si ha pasado el retardo para dibujar una nueva postura
            if self.currentDelay < 0:
                # Actualizamos la postura
                self.animationFrame += 1

                # Reiniciamos la animación si nos hemos pasado de frames
                if self.animationFrame >= len(currentAnim):
                    if self.animationLoop:
                        self.animationFrame = 0
                    else:
                        self.animationFrame -= 1
                        self.animationFinish = True

                # Actualizamos el delay
                self.currentDelay = currentAnim[self.animationFrame]['delay']

                # Actualiamos la imagen con el frame correspondiente
                self.origImage = self.sheet.subsurface(currentAnim[self.animationFrame]['coords'])
                self.image = self.origImage.copy()
                self.rect.size = self.image.get_size()

                # Máscara de la animación
                self.mask = pygame.mask.from_surface(self.image)
