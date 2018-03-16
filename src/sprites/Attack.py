# -*- coding: utf-8 -*-

import pygame, sys, os, math

from src.ResourceManager import *
from src.sprites.MySprite import *

# -------------------------------------------------
# Sprites de ataques
class Attack(MySprite):
    @classmethod
    def calc_rot_pos(cls, ang, r, width, height, Pj):
        if (ang>=0):
            if (ang<90): # Cuadrante I
                Pc = calc_triang(Pj, r, ang, 0, 1, -1)
                Pl = calc_triang(Pc, width/2, ang, 1, -1, -1)
                Pe = calc_triang(Pl, height, ang, 0, 0, -1)
            else: # Cuadrante II
                Pc = calc_triang(Pj, r, ang, 0, 1, -1)
                Pl1 = calc_triang(Pc, width/2, ang, 1, -1, -1)
                Pl2 = calc_triang(Pl1, height, ang, 0, 1, -1)
                Pe = calc_triang(Pl2, height, ang, 1, 0, 1)
        else:
            if (ang>-90): # Cuadrante IV
                Pc = calc_triang(Pj, r, ang, 0, 1, -1)
                Pl = calc_triang(Pc, width/2, ang, 1, -1, -1)
                Pe = calc_triang(Pl, height, ang, 1, 1, 0)
            else: # Cuadrante III
                Pc = calc_triang(Pj, r, ang, 0, 1, -1)
                Pl = calc_triang(Pc, width/2, ang, 1, 1, 1)
                Pe = calc_triang(Pl, height, ang, 0, 1, 0)
        return Pe

    def __init__(self, imageFile, spriteSheet, enemyGroup):
        # Primero invocamos al constructor de la clase padre
        MySprite.__init__(self)

        # Cargar sheet de sprites
        self.sheet = ResourceManager.load_image(imageFile, -1)

        # Leer coordenadas de fichero
        data = ResourceManager.load_sprite_sheet(spriteSheet)
        self.sheetConf = []
        # Cargamos los sprites
        for col in range(0, len(data)):
            cell = data[col]
            coords = pygame.Rect((int(cell['left']), int(cell['top'])), (int(cell['width']), int(cell['height'])))
            delay = float(cell['delay'])*1000
            self.sheetConf.append({'coords': coords, 'delay': delay})

        # Animación inicial
        self.animationFrame = 0
        self.currentDelay = 0

        self.drawAnimation = True

        self.rect = pygame.Rect(0, 0, self.sheetConf[0]['coords'][2], self.sheetConf[0]['coords'][3])

        # Frame inicial
        self.origImage = self.sheet.subsurface(self.sheetConf[0]['coords'])
        self.image = self.origImage

        # Máscara de la animación
        self.mask = pygame.mask.from_surface(self.origImage)

        self.enemyGroup = enemyGroup

    def update_animation(self, time):
        if self.drawAnimation:
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
                    self.drawAnimation = False

                # Actualiamos la imagen con el frame correspondiente
                self.origImage = self.sheet.subsurface(self.sheetConf[self.animationFrame]['coords'])

                self.rect.width = self.origImage.get_width()
                self.rect.height = self.origImage.get_height()

                self.mask = pygame.mask.from_surface(self.origImage)

    def update(self, time):
        # Actualizamos la imagen a mostrar
        self.update_animation(time)

        # Colisiones
        if self.drawAnimation:
            for enemy in self.enemyGroup:
                (atkX, atkY) = self.position
                (enemyX, enemyY) = enemy.position
                atkY -= self.image.get_height()
                enemyY -= enemy.image.get_height()
                offset = (int(enemyX - atkX), int(enemyY - atkY))
                collision = self.mask.overlap(enemy.mask, offset)
                if collision is not None:
                    print('Hit')

    def draw(self, surface):
        if self.drawAnimation:
            surface.blit(self.image, self.rect)

# Método para calcular triángulos
# recibe un punto, la hipotenusa y el ángulo
# invAB es para utilizar el lado b en lugar del a y vice.
# paramX e Y se multiplican por los lados para conseguir
# diferentes configuraciones (sumar, restar, 0)
# devuelve el punto calculado
def calc_triang(P, h, ang, invAB, paramX, paramY):
    ladoA = h * math.sin(math.radians(ang))
    ladoB = h * math.cos(math.radians(ang))
    x,y = P
    if (invAB):
        newP = (x+ladoA*paramX, y+ladoB*paramY)
    else:
        newP = (x+ladoB*paramX, y+ladoA*paramY)
    return newP
