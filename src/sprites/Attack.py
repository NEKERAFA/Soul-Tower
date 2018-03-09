# -*- coding: utf-8 -*-

import pygame, sys, os, math

from src.ResourceManager import *
from src.sprites.MySprite import *

# -------------------------------------------------
# Sprites de ataques
class Attack(MySprite):
    @classmethod
    def calcRotPos(cls, ang, r, width, height, Pj):
        if (ang>=0):
            if (ang<90): # Cuadrante I
                Pc = calcTriang(Pj, r, ang, 0, 1, -1)
                Pl = calcTriang(Pc, width/2, ang, 1, -1, -1)
                Pe = calcTriang(Pl, height, ang, 0, 0, -1)
            else: # Cuadrante II
                Pc = calcTriang(Pj, r, ang, 0, 1, -1)
                Pl1 = calcTriang(Pc, width/2, ang, 1, -1, -1)
                Pl2 = calcTriang(Pl1, height, ang, 0, 1, -1)
                Pe = calcTriang(Pl2, height, ang, 1, 0, 1)
        else:
            if (ang>-90): # Cuadrante IV
                Pc = calcTriang(Pj, r, ang, 0, 1, -1)
                Pl = calcTriang(Pc, width/2, ang, 1, -1, -1)
                Pe = calcTriang(Pl, height, ang, 1, 1, 0)
            else: # Cuadrante III
                Pc = calcTriang(Pj, r, ang, 0, 1, -1)
                Pl = calcTriang(Pc, width/2, ang, 1, 1, 1)
                Pe = calcTriang(Pl, height, ang, 0, 1, 0)
        return Pe

    def __init__(self, imageFile, spriteSheet, enemyGroup):
        # Primero invocamos al constructor de la clase padre
        MySprite.__init__(self)

        # Cargar sheet de sprites
        self.sheet = ResourceManager.load_image(imageFile, -1)
        self.sheet = self.sheet.convert_alpha()

        # Leer coordenadas de fichero
        data = ResourceManager.load_sprite_sheet(spriteSheet)
        self.sheetConf = []
        # Cargamos los sprites
        for col in range(0, len(data)):
            cell = data[col]
            #print(cell)
            coords = pygame.Rect((int(cell['left']), int(cell['top'])), (int(cell['width']), int(cell['height'])))
            delay = float(cell['delay'])*1000
            self.sheetConf.append({'coords': coords, 'delay': delay})

        # Animación inicial
        self.animationFrame = 0
        self.currentDelay = 0

        self.drawAnimation = True

        self.width = self.sheetConf[self.animationFrame]['coords'][2]
        self.height = self.sheetConf[self.animationFrame]['coords'][3]
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rotation = 0

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

            # Miramos si ha pasa[self.animationNum]do el retardo para dibujar una nueva postura
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
            #print("drawing")

# Método para calcular triángulos
# recibe umn punto, la hipotenusa y el ángulo
# invAB es para utilizar el lado b en lugar del a y vice.
# paramX e Y se multiplican por los lados para conseguir
# diferentes configuraciones (sumar, restar, 0)
# devuelve el punto calculado
def calcTriang(P, h, ang, invAB, paramX, paramY):
    lado_a = h * math.sin(math.radians(ang))
    lado_b = h * math.cos(math.radians(ang))
    x,y = P
    if (invAB):
        newP = (x+lado_a*paramX, y+lado_b*paramY)
    else:
        newP = (x+lado_b*paramX, y+lado_a*paramY)
    return newP
