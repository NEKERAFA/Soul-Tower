# -*- coding: utf-8 -*-

import pygame, sys, os
import math as m

from pygame.locals import *
from src.ResourceManager import *
from src.sprites.MySprite import *
from src.sprites.Force import *

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

CHARACTER_PATH = 'characters'

# -------------------------------------------------
# Sprites de personajes
class Character(MySprite):
    '''
        Parámetros pasados al constructor de esta clase:
            * Nombre del sprite
    '''
    def __init__(self, imageFile, spriteSheet):
        # Primero invocamos al constructor de la clase padre
        MySprite.__init__(self)

        # Cargar sheet de sprites
        self.sheet = ResourceManager.load_image(os.path.join('sprites', CHARACTER_PATH, imageFile), -1)

        # Movimiento actual
        self.movement = STILL

        # Lado hacia el que está mirando
        self.looking = W

        # Leer el fichero de configuración
        data = ResourceManager.load_sprite_conf(os.path.join(CHARACTER_PATH, spriteSheet))

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

        # Cargamos los estados de comportamiento posibles
        if "behaviour" in data:
            self.behaviour = data["behaviour"]
        else:
            self.behaviour = None

        # Animación inicial
        self.animationNum = SPRITE_STILL
        self.animationFrame = 0

        # El rectangulo del Sprite
        self.rect = pygame.Rect(0, 0, self.sheetConf[0][0]['coords'][2], self.sheetConf[0][0]['coords'][3])

        # La velocidad de caminar en diagonal
        self.diagonalSpeed = m.sqrt((self.stats["spd"] * self.stats["spd"])/2.0)

        # Aceleración inicial
        self.aceleration = None
        self.decrement = 0

        # Frame inicial
        self.origImage = self.sheet.subsurface(self.sheetConf[0][0]['coords'])
        self.image = self.origImage.copy()

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
            self.origImage = self.sheet.subsurface(currentAnim[self.animationFrame]['coords'])
            self.image = self.origImage.copy()
            self.rect.size = self.image.get_size()

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

        # Comprobamos si existe una aceleración para aplicarsela a cada eje
        if self.aceleration is not None:
            (acelX, acelY) = self.aceleration.get_coordinates()
            speedX = acelX*time
            speedY = acelY*time

            self.aceleration.substrat(self.decrement)

            if self.aceleration.magnitude <= 0:
                self.aceleration = None
                self.decrement = 0

        # Aplicamos la velocidad en cada eje
        self.speed = (speedX, speedY)

    def update(self, time, mapRect, mapMask):
        # Actualizamos todo lo del movimiento y la animación
        self.update_movement(time)

        # Y llamamos al método de la superclase para que, según la velocidad y el tiempo, calcule la nueva posición del Sprite
        MySprite.update(self, time)

        self.fix_collision(mapRect, mapMask)

    # TODO: ya no hace falta mapRect
    def fix_collision(self, mapRect, mapMask):
        # Después se utiliza la máscara para un ajuste más preciso
        x, y = self.rect.topleft

        # Se calculan los "gradientes" para conocer la dirección de la colisión
        dx = mapMask.overlap_area(self.mask,(x+1,y)) - mapMask.overlap_area(self.mask,(x-1,y))
        dy = mapMask.overlap_area(self.mask,(x,y+1)) - mapMask.overlap_area(self.mask,(x,y-1))

        # Se desplaza el personaje en la dirección adecuada
        # hasta que deje de colisionar
        while(dx or dy):
            if (dx>0):
                incrX = -1
            elif (dx<0):
                incrX = 1
            else:
                incrX = 0
            if (dy>0):
                incrY = -1
            elif (dy<0):
                incrY = 1
            else:
                incrY = 0
            self.increment_position((incrX, incrY))
            x, y = self.rect.topleft
            dx = mapMask.overlap_area(self.mask, (x+1,y)) - mapMask.overlap_area(self.mask, (x-1,y))
            dy = mapMask.overlap_area(self.mask, (x,y+1)) - mapMask.overlap_area(self.mask, (x,y-1))


    ############################################################################

    def apply_force(self, angle, radius, decrement):
        self.aceleration = Force(angle, radius)
        self.decrement = decrement

    # Recibe un daño y se realiza el daño. Si el personaje ha muerto, lo elimina
    # de todos los grupos
    def receive_damage(self, damage, angle):
        self.stats["hp"] -= damage

        if self.stats["hp"] <= 0:
            self.kill()

        # self.apply_force(angle, self.stats["spd"]/16, self.stats["spd"]/64)
        # TODO: cambio provisional para que los enemigos reboten decentemente
        # debería ser un stat
        self.apply_force(angle, 0.0125, 0.003125)

    # Añade vidas al personaje
    def add_lifes(self, lifes):
        self.stats["hp"] = max(self.stats["max_hp"], self.stats["hp"]+lifes)
