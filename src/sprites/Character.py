# -*- coding: utf-8 -*-

import pygame, sys, os
import math as m

from pygame.locals import *
from src.ResourceManager import *
from src.sprites.MySprite import *

# -------------------------------------------------
# -------------------------------------------------
# Constantes
# -------------------------------------------------
# -------------------------------------------------

# Movimientos
STILL = 0
W = 1
E = 2
N = 3
S = 4
NW = 5
NE = 6
SW = 7
SE = 8

# Animaciones
SPRITE_STILL = 0
SPRITE_WALKING_UP = 1
SPRITE_WALKING_DOWN = 2
SPRITE_WALKING = 3

# -------------------------------------------------
# Sprites de personajes
class Character(MySprite):
    '''
        Parámetros pasados al constructor de esta clase:
            * Nombre del sprite
            * Velocidad de caminar en los ejes x e y (no diagonal)
    '''
    def __init__(self, spriteName):
        # Primero invocamos al constructor de la clase padre
        MySprite.__init__(self)

        # Obtenemos el nombre de la carpeta del sprite sheet y del archivo de configuración
        fullname = os.path.join('characters', spriteName)
        imagePath = os.path.join('sprites', fullname) + '.png'

        # Cargar sheet de sprites
        self.sheet = ResourceManager.load_image(imagePath, -1)

        # Movimiento actual
        self.movement = STILL

        # Lado hacia el que está mirando
        self.looking = W

        # Leer el fichero de configuración
        data = ResourceManager.load_sprite_conf(fullname + '.json')

        # Cargamos los sprites
        self.sheetConf = []
        for row in range(0, len(data["frames"])):
            self.sheetConf.append([])
            tmp = self.sheetConf[row]
            for cell in data["frames"][row]:
                # Creamos las coordenadas
                coords = pygame.Rect((int(cell['x']), int(cell['y'])), (int(cell['width']), int(cell['height'])))
                # Cargamos el delay y lo convertimos en milisegundos
                delay = float(cell['delay'])*1000
                # Guardamos la configuración
                tmp.append({'coords': coords, 'delay': delay})

        # Cargamos los stats
        self.stats = data["stats"]

        # Animación inicial
        self.animationNum = SPRITE_STILL
        self.animationFrame = 0

        # El rectangulo del Sprite
        self.rect = pygame.Rect(0, 0, self.sheetConf[0][0]['coords'][2], self.sheetConf[0][0]['coords'][3])

        # La velocidad de caminar en diagonal
        self.diagonalSpeed = m.sqrt((self.stats["spd"] * self.stats["spd"])/2.0)

        # Frame inicial
        self.image = self.sheet.subsurface(self.sheetConf[0][0]['coords'])

        # Delay actual
        self.currentDelay = self.sheetConf[0][0]['delay']

        # Máscara de la animación
        self.mask = pygame.mask.from_surface(self.image)

    # Metodo base para realizar el movement: simplemente se le indica cual va
    # a hacer, y lo almacena
    def move(self, movement):
        self.movement = movement

    def update_animation(self, time):
        # Actualizamos el retardo
        self.currentDelay -= time
        currentAnim = self.sheetConf[self.animationNum]

        # Miramos si ha pasado el retardo para dibujar una nueva postura
        if self.currentDelay < 0:
            # Actualizamos la postura
            self.animationFrame += 1

            # Reiniciamos la animación si nos hemos pasado de frames
            if self.animationFrame >= len(currentAnim):
                self.animationFrame = 0

            # Actualizamos el delay
            self.currentDelay = currentAnim[self.animationFrame]['delay']

            # Actualiamos la imagen con el frame correspondiente
            self.image = self.sheet.subsurface(currentAnim[self.animationFrame]['coords'])
            self.rect.width = self.image.get_width()
            self.rect.height = self.image.get_height()

            # Si mira a la E, invertimos esa imagen
            if self.looking == E:
                self.image = pygame.transform.flip(self.image, 1, 0)

            # Máscara de la animación
            self.mask = pygame.mask.from_surface(self.image)



    def update_movement(self, time):
        # Las velocidades a las que iba hasta este momento
        # (speedX, speedY) = self.speed
        speedX, speedY = 0, 0

        # Primero diferenciamos quieto y caminando para la animación
        # Después, diferenciamos todas las direcciones para asignarles
        # la velocidad correspondiente a los ejes
        if (self.movement == STILL):
            # Actualizamos el movimiento
            if self.animationNum != SPRITE_STILL:
                self.animationNum = SPRITE_STILL
                self.currentDelay = 0
                self.animationFrame = 0
        elif (self.movement == N):
            if self.animationNum != SPRITE_WALKING_UP:
                self.animationNum = SPRITE_WALKING_UP
                self.currentDelay = 0
                self.animationFrame = 0
            speedY = -self.stats["spd"]
        elif (self.movement == S):
            if self.animationNum != SPRITE_WALKING_DOWN:
                self.animationNum = SPRITE_WALKING_DOWN
                self.currentDelay = 0
                self.animationFrame = 0
            speedY = self.stats["spd"]
        else:
            if self.animationNum != SPRITE_WALKING:
                self.animationNum = SPRITE_WALKING
                self.currentDelay = 0
                self.animationFrame = 0

            if (self.movement == NW):
                self.looking = W
                speedX = -self.diagonalSpeed
                speedY = -self.diagonalSpeed
            elif (self.movement == NE):
                self.looking = E
                speedX = self.diagonalSpeed
                speedY = -self.diagonalSpeed
            elif (self.movement == W):
                self.looking = W
                speedX = -self.stats["spd"]
            elif (self.movement == E):
                self.looking = E
                speedX = self.stats["spd"]
            elif (self.movement == SW):
                self.looking = W
                speedX = -self.diagonalSpeed
                speedY = self.diagonalSpeed
            elif (self.movement == SE):
                self.looking = E
                speedX = self.diagonalSpeed
                speedY = self.diagonalSpeed

        # Actualizamos la imagen a mostrar
        self.update_animation(time)

        # Aplicamos la velocidad en cada eje
        self.speed = (speedX, speedY)


    def update(self, time, mapRect, mapMask):

        # Actualizamos todo lo del movimiento y la animación
        self.update_movement(time)

        # Y llamamos al método de la superclase para que, según la velocidad y el tiempo, calcule la nueva posición del Sprite
        MySprite.update(self, time)

        x, y = self.position
        x = int(x)
        y = int(y - self.rect.height)

        # Se calculan los "gradientes" para conocer la dirección de la colisión
        dx = mapMask.overlap_area(self.mask,(x+1,y)) - mapMask.overlap_area(self.mask,(x-1,y))
        dy = mapMask.overlap_area(self.mask,(x,y+1)) - mapMask.overlap_area(self.mask,(x,y-1))

        # Se desplaza el personaje en la dirección adecuada
        # hasta que deje de colisionar
        while(dx):
            self.increment_position(((1 if dx<0 else -1), 0))
            x,y = self.position
            x = int(x)
            y = int(y - self.rect.height)
            dx = mapMask.overlap_area(self.mask, (x+1,y)) - mapMask.overlap_area(self.mask, (x-1,y))

        while(dy):
            self.increment_position((0,(1 if dy<0 else -1)))
            x,y = self.position
            x = int(x)
            y = int(y - self.rect.height)
            dy = mapMask.overlap_area(self.mask, (x,y+1)) - mapMask.overlap_area(self.mask, (x,y-1))

    ############################################################################

    # Recibe un daño y se realiza el daño. Si el personaje a muerto, LO MATA
    def receive_damage(self, damage):
        self.stats["hp"] -= damage

        if self.stats["hp"] <= 0:
            self.kill()
