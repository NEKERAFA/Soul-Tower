# -*- coding: utf-8 -*-

import pygame, sys, os
from pygame.locals import *
from src.ResourceManager import *
from src.sprites.MySprite import *
import math as m


imageFile = 'Jugador.png'
spriteSheet = 'coordJugador.txt'
R = 30

class MeleeManager(MySprite):
    def __init__(self, sheet, sheetCoords):
        MySprite.__init__(self)
        self.position = (0,0)
        self.rotation = 0
        self.attacking = 0
        self.elapsed_time = 0
        self.animating = 0
        self.atk_enabled = 0
        self.frame = 0
        self.anim_time = 0

        # Cargar sheet de sprites

        self.orig_image = sheet.subsurface(sheetCoords[0][0]['coords'])
        self.image = self.orig_image
        self.width = sheetCoords[0][0]['coords'][2]
        self.height = sheetCoords[0][0]['coords'][3]

    def startAttack(self, position, rotation):
        self.attacking = 1
        self.position = calcRotPos(rotation, R, self.width, self.height, position)
        self.rotation = rotation
        # print(self.rotation)

    def endAttack(self):
        self.attacking = 0

    def draw(self, screen):
        # print(self.attacking, self.atk_enabled)
        # Si se debe atacar, se indica que se debe animar
        if self.attacking and self.atk_enabled:
            self.animating = 1
        # mientras no se llegue al tiempo de animación, se hace blit
        if (self.animating):
            if (self.anim_time < 150):
                self.image = pygame.transform.rotate(self.orig_image, self.rotation)
                screen.blit(self.image, self.position)
                self.anim_time += self.elapsed_time
            else:
                self.anim_time = 0
                self.animating = 0

    def update(self, time):
        # Si ha pasado el tiempo suficiente y estamos atacando
        if ((self.elapsed_time > 250) and (self.attacking)):
            # tenemos que animar
            self.atk_enabled = 1
            # y reiniciar el contador
            self.elapsed_time = 0
        # si no
        else:
            # aumentamos el tiempo
            self.elapsed_time += time
            self.atk_enabled = 0


def calcRotPos(ang, r, width, height, Pj):
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

# Método para calcular triángulos
# recibe un punto, la hipotenusa y el ángulo
# invAB es para utilizar el lado b en lugar del a y vice.
# paramX e Y se multiplican por los lados para conseguir
# diferentes configuraciones (sumar, restar, 0)
# devuelve el punto calculado
def calcTriang(P, h, ang, invAB, paramX, paramY):
    lado_a = h * m.sin(m.radians(ang))
    lado_b = h * m.cos(m.radians(ang))    
    x,y = P
    if (invAB):
        newP = (x+lado_a*paramX,y+lado_b*paramY)
    else:
        newP = (x+lado_b*paramX,y+lado_a*paramY)
    return newP

