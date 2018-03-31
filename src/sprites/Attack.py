# -*- coding: utf-8 -*-

import pygame, sys, os, math

from src.ResourceManager import *
from src.sprites.MySprite import *

ATTACK_PATH = 'attacks'
# -------------------------------------------------
# Sprites de ataques
class Attack(MySprite):
    @classmethod
    def calc_rot_pos(cls, ang, r, width, height, Pj):
        if (ang>=0):
            if (ang<90): # Cuadrante I
                Pc = cls.calc_triang(Pj, r, ang, 0, 1, -1)
                Pl = cls.calc_triang(Pc, height/2, ang, 1, -1, -1)
                Pe = cls.calc_triang(Pl, width, ang, 0, 0, -1)
            else: # Cuadrante II
                Pc = cls.calc_triang(Pj, r, ang, 0, 1, -1)
                Pl1 = cls.calc_triang(Pc, height/2, ang, 1, -1, -1)
                Pl2 = cls.calc_triang(Pl1, width, ang, 0, 1, -1)
                Pe = cls.calc_triang(Pl2, height, ang, 1, 0, 1)
        else:
            if (ang>-90): # Cuadrante IV
                Pc = cls.calc_triang(Pj, r, ang, 0, 1, -1)
                Pl = cls.calc_triang(Pc, height/2, ang, 1, -1, -1)
                Pe = cls.calc_triang(Pl, height, ang, 1, 1, 0)
            else: # Cuadrante III
                Pc = cls.calc_triang(Pj, r, ang, 0, 1, -1)
                Pl = cls.calc_triang(Pc, height/2, ang, 1, 1, 1)
                Pe = cls.calc_triang(Pl, width, ang, 0, 1, 0)
        return Pe

    # Método para calcular triángulos
    # recibe un punto, la hipotenusa y el ángulo
    # invAB es para utilizar el lado b en lugar del a y vice.
    # paramX e Y se multiplican por los lados para conseguir
    # diferentes configuraciones (sumar, restar, 0)
    # devuelve el punto calculado
    @classmethod
    def calc_triang(cls, P, h, ang, invAB, paramX, paramY):
        ladoA = h * math.sin(math.radians(ang))
        ladoB = h * math.cos(math.radians(ang))
        x,y = P
        if (invAB):
            newP = (x+ladoA*paramX, y+ladoB*paramY)
        else:
            newP = (x+ladoB*paramX, y+ladoA*paramY)
        return newP

    def __init__(self, imageFile, spriteSheet, enemies, effect_sound):
        # Primero invocamos al constructor de la clase padre
        MySprite.__init__(self)

        # Cargar sheet de sprites
        self.sheet = ResourceManager.load_image(os.path.join('sprites', ATTACK_PATH, imageFile), -1)

        #Cargamos efecto de sonido
        self.effect_sound = ResourceManager.load_effect_sound(effect_sound)

        # Leer coordenadas de fichero
        data = ResourceManager.load_sprite_conf(os.path.join(ATTACK_PATH, spriteSheet))
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

        # Controlamos la animación y si está en loop o no
        self.drawAnimation = True
        self.loopAnimation = False

        self.rect = pygame.Rect(0, 0, self.sheetConf[0]['coords'][2], self.sheetConf[0]['coords'][3])

        # Frame inicial
        self.origImage = self.sheet.subsurface(self.sheetConf[0]['coords'])
        self.image = self.origImage.copy()
        self.rotation = 0

        # Máscara de la animación
        self.mask = pygame.mask.from_surface(self.origImage)

        self.enemies = enemies

        # Para llevar cuenta del nº de ataque
        self.id = 0

    def update_animation(self, time):
        if self.loopAnimation or self.drawAnimation:
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
                    self.id += 1

                # Actualiamos la imagen con el frame correspondiente
                self.origImage = self.sheet.subsurface(self.sheetConf[self.animationFrame]['coords'])
                self.image = self.origImage.copy()

                self.rect.width = self.origImage.get_width()
                self.rect.height = self.origImage.get_height()

                self.mask = pygame.mask.from_surface(self.origImage)

    def update(self, time):
        # Actualizamos la imagen a mostrar
        self.update_animation(time)

    def draw(self, surface):
        # Mostramos la animación si se debería de mostrar
        if self.drawAnimation:
            surface.blit(self.image, self.rect)
