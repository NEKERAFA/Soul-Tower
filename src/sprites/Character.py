# -*- coding: utf-8 -*-

import pygame, sys, os
import math as m

from pygame.locals import *
from src.ResourceManager import *
from src.controls.KeyboardMouseControl import *
from src.sprites.MySprite import *

# -------------------------------------------------
# -------------------------------------------------
# Constantes
# -------------------------------------------------
# -------------------------------------------------

# movimientos
STILL = 0
W = 1
E = 2
N = 3
S = 4
NW = 5
NE = 6
SW = 7
SE = 8

# animaciones
SPRITE_STILL = 0
SPRITE_WALKING = 1

# -------------------------------------------------
# Sprites de personajes
class Character(MySprite):
    # Parámetros pasados al constructor de esta clase:
    #  Archivo con la sheet de Sprites
    #  Archivo con las coordenadoas dentro de la sheet
    #  Numero de imagenes en cada postura
    #  Velocidad de caminar en los ejes x e y (no diagonal)
    #  Retardo para mostrar la animacion del personaje
    #def __init__(self, archivoImagen, archivoCoordenadas, numImagenes, speed, velocidadSalto, retardoAnimacion):
    # TODO: cambiar spritesheet en UML por spriteSheet e image por imageFile y speed por playerSpeed
    def __init__(self, imageFile, spriteSheet, numImages, playerSpeed, animationDelay):
        MySprite.__init__(self);
        # TODO: añadir atributos al UML

        # Cargar sheet de sprites
        self.sheet = ResourceManager.load_image(imageFile,-1)
        self.sheet = self.sheet.convert_alpha()
        # movement actual
        self.movement = STILL
        # Lado hacia el que está mirando
        self.looking = W

        # Leer coordenadas de fichero
        data = ResourceManager.load_coordinates_file(spriteSheet)
        data = data.split()
        cont = 0;
        self.sheetCoords = [];
        for row in range(0, 3):
            self.sheetCoords.append([])
            tmp = self.sheetCoords[row]
            for animation in range(1, numImages[row]+1):
                tmp.append(pygame.Rect((int(data[cont]), int(data[cont+1])), (int(data[cont+2]), int(data[cont+3]))))
                cont += 4

        # Retraso actual entre animaciones. (Se va reiniciando cuando llega a animationDelay)
        self.currentDelay = 0;

        # Animación inicial
        self.animationNum = SPRITE_STILL
        self.animationFrame = 0;

        # El rectangulo del Sprite
        self.rect = pygame.Rect(100,100,self.sheetCoords[self.animationNum][self.animationFrame][2],self.sheetCoords[self.animationNum][self.animationFrame][3])

        # La velocidad de caminar en x e y (no diagonal)
        self.playerSpeed = playerSpeed
        self.diagonalSpeed = m.sqrt((playerSpeed * playerSpeed)/2.0)

        # El retardo en la animacion del personaje (podria y deberia ser distinto para cada postura)
        self.animationDelay = animationDelay

        # Y actualizamos la postura del Sprite inicial, llamando al metodo correspondiente
        self.update_animation()


    # Metodo base para realizar el movement: simplemente se le indica cual va a hacer, y lo almacena
    def move(self, movement):
        self.movement = movement

    def update_animation(self):
        self.currentDelay -= 1
        # Miramos si ha pasado el retardo para dibujar una nueva postura
        if (self.currentDelay < 0):
            self.currentDelay = self.animationDelay
            # Si ha pasado, actualizamos la postura
            self.animationFrame += 1
            if self.animationFrame >= len(self.sheetCoords[self.animationNum]):
                self.animationFrame = 0;
            if self.animationFrame < 0:
                self.animationFrame = len(self.sheetCoords[self.animationNum])-1
            self.image = self.sheet.subsurface(self.sheetCoords[self.animationNum][self.animationFrame])

            # Si esta mirando a la izquiera, cogemos la porcion de la sheet
            if self.looking == W:
                self.image = self.sheet.subsurface(self.sheetCoords[self.animationNum][self.animationFrame])
            #  Si no, si mira a la E, invertimos esa imagen
            elif self.looking == E:
                self.image = pygame.transform.flip(self.sheet.subsurface(self.sheetCoords[self.animationNum][self.animationFrame]), 1, 0)

    #TODO: cambiar mask de UML a mapMask
    def update(self, mapMask, time):

        # Las velocidades a las que iba hasta este momento
        (speedX, speedY) = self.speed

        # Primero diferenciamos quieto y caminando para la animación
        # Después, diferenciamos todas las direcciones para asignarles
        # la velocidad correspondiente a los ejes
        if (self.movement == STILL):
            self.animationNum = SPRITE_STILL
            speedX = 0
            speedY = 0
        else:
            self.animationNum = SPRITE_WALKING
            if (self.movement == NW):
                self.looking = W
                speedX = -self.diagonalSpeed
                speedY = -self.diagonalSpeed
            elif (self.movement == N):
                speedX = 0
                speedY = -self.playerSpeed
            elif (self.movement == NE):
                self.looking = E
                speedX = self.diagonalSpeed
                speedY = -self.diagonalSpeed
            elif (self.movement == W):
                self.looking = W
                speedX = -self.playerSpeed
                speedY = 0;
            elif (self.movement == E):
                self.looking = E
                speedX = self.playerSpeed
                speedY = 0
            elif (self.movement == SW):
                self.looking = W
                speedX = -self.diagonalSpeed
                speedY = self.diagonalSpeed
            elif (self.movement == S):
                speedX = 0
                speedY = self.playerSpeed
            elif (self.movement == SE):
                self.looking = E
                speedX = self.diagonalSpeed
                speedY = self.diagonalSpeed


        # Actualizamos la imagen a mostrar
        self.update_animation()

        # Aplicamos la velocidad en cada eje
        self.speed = (speedX, speedY)

        # Y llamamos al método de la superclase para que, según la velocidad y el tiempo
        #  calcule la nueva posición del Sprite
        MySprite.update(self, time)

        #TODO:
        # Aquí comprobarías con la máscara si estás fuera del mapa y con una función mágica calculas la posición en la que deberías estar

        return
