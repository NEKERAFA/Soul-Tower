# -*- coding: utf-8 -*-

import pygame, sys, os
import math as m
import random

from pygame.locals import *
from src.ResourceManager import *
from src.sprites.MySprite import *
from src.sprites.Force import *
from src.Channel_Effect import *

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
    def __init__(self, imageFile, spriteSheet, loadStats=None):
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


        #Cargamos el sonido del movimiento
        self.sound_movement = ResourceManager.load_effect_sound(data["sound"])
        #Cargamos el sonido de la muerte
        self.dead_sound = ResourceManager.load_effect_sound(data["dead_sound"])
        #Reservamos un canal
        pygame.mixer.set_reserved(2)
        chanel_reserved_0 = pygame.mixer.Channel(0)
        self.dead_chanel = pygame.mixer.Channel(1)
        #Establecemos delay
        delay_sound = random.randint(3, 4)*1000
        #Lo pasamos al channel_effect
        self.channel_effect = Channel_Effect(self.sound_movement,chanel_reserved_0, delay_sound)

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
        if(loadStats is not None):
            self.stats = loadStats
        else:
            self.stats = data["stats"].copy()

        # Cargamos los estados de comportamiento posibles
        if "behaviour" in data:
            self.behaviour = data["behaviour"]

        self.origImage = pygame.Surface((0, 0))
        self.image = self.origImage.copy()

        # El rectangulo del Sprite
        self.rect = self.image.get_rect().copy()

        # Delay actual
        self.currentDelay = 0

        # Máscara de la animación
        self.mask = None

        # Animación inicial
        self.set_initial_frame(SPRITE_STILL)

        # La velocidad de caminar en diagonal
        self.diagonalSpeed = m.sqrt((self.stats["spd"] * self.stats["spd"])/2.0)

        # Aceleración inicial
        self.impulse = None

        # Define si el sprite está muerto o no
        self.killed = False

        # Para ver si la animación se tiene que loopear o no
        self.animationLoop = True

        # La animación ha terminado
        self.animationFinish = False

    def set_initial_frame(self, animationNum):
        # Establecemos la animación
        self.animationNum = animationNum
        self.animationFrame = 0

        # Primer frame
        firstFrame = self.sheetConf[self.animationNum][self.animationFrame]

        # Frame inicial
        self.origImage = self.sheet.subsurface(firstFrame['coords'])
        self.image = self.origImage.copy()
        if self.looking == E:
            self.image = pygame.transform.flip(self.image, 1, 0)

        # El rectangulo del Sprite
        self.rect.size = self.image.get_size()

        # Delay actual
        self.currentDelay = firstFrame['delay']

        # Máscara de la animación
        self.mask = pygame.mask.from_surface(self.image)

    # Metodo base para realizar el movement: simplemente se le indica cual va
    # a hacer, y lo almacena
    def move(self, movement):
        self.movement = movement

    def update_animation(self, time):
        if self.animationLoop or not self.animationFinish:
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
        if self.impulse is not None:
            (acelX, acelY) = self.impulse.get_coordinates()
            speedX = acelX*time
            speedY = acelY*time

            self.impulse.substrat()

            if self.impulse.magnitude <= 0:
                self.impulse = None

        # Aplicamos la velocidad en cada eje
        self.speed = (speedX, speedY)

    def update(self, time, mapRect, mapMask):
        #Actualizamos el sonido
        self.channel_effect.soundUpdate(time)
        # Actualizamos todo lo del movimiento y la animación
        self.update_movement(time)

        # Y llamamos al método de la superclase para que, según la velocidad y el tiempo, calcule la nueva posición del Sprite
        MySprite.update(self, time)

        self.fix_collision(mapMask)

    def fix_collision(self, mapMask):
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

    def apply_force(self, force):
        self.impulse = force

    # Recibe un daño y se realiza el daño. Si el personaje ha muerto, lo elimina
    # de todos los grupos
    def receive_damage(self, damage, force):
        # Reducimos el daño
        self.stats["hp"] -= damage

        # Si la vida llega a cero lo matamos
        if self.stats["hp"] <= 0:
            self.killed = True

        if force!=0:
            # Aplicamos una fuerza de rebote
            self.apply_force(force)

    # Añade vidas al personaje
    def add_lifes(self, lifes):
        self.stats["hp"] = min(self.stats["max_hp"], self.stats["hp"]+lifes)
