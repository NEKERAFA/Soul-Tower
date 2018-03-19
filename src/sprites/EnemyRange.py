# -*- coding: utf-8 -*-

import pygame, math
from src.ResourceManager import *
from src.sprites.MyStaticSprite import *
from src.sprites.Character import *

# -------------------------------------------------
# Clase EnemyRange

class EnemyRange(MyStaticSprite):
    def __init__(self, center, radius, angle, lookAt):
        '''
            center: (int, int), Centro del cono de visión
            radius: int, Radio del cono de visión
            angle: float, Ángulo de apertura del cono visión
            lookAt: int, Ángulo hacia donde mira al iniciarse
        '''
        # Llamamos al constructor de la superclase
        MyStaticSprite.__init__(self)
        # Guardo el radio y el ángulo de vision
        self.radius = radius
        self.angle = angle
        # Creamos la imagen para hacer el mapa y la pintamos de negro
        self.image = pygame.Surface((radius*2, radius*2))
        # Establecemos el rectángulo
        self.rect = self.image.get_rect()
        self.rect.center = center
        # Obtengo los puntos del polígono
        arc = EnemyRange.get_slice_circle((radius, radius), radius, angle)
        # Dibujo el arco que actuará como campo de visión
        pygame.draw.polygon(self.image, (255, 255, 255), arc)
        # Convierto lo negro a transparente
        self.image.set_colorkey((0, 0, 0))
        # Creo la máscara
        self.look_at(lookAt)
        self.lookAt = lookAt

    def look_at(self, angle):
        '''
            Rota el cono de visión al ángulo indicado
        '''
        self.lookAt = angle
        center = self.rect.center
        # Roto la imagen para cargarla como máscara
        rotImage = pygame.transform.rotate(self.image, self.lookAt)
        self.rect = rotImage.get_rect()
        self.rect.center = center
        # Creo la máscara con la imagen rotada
        self.mask = pygame.mask.from_surface(rotImage)

    def get_delta(self):
        '''
            Obtiene el desplazamiento desde el punto de arriba a la izquierda al
            centro de la imagen del rango de visión
        '''
        x, y = self.rect.topleft
        centerX, centerY = self.rect.center
        return (centerX-x, centerY-y)

    @classmethod
    def get_slice_circle(cls, center, radius, angle, slices=32):
        '''
            Obtiene una lista de puntos que representan un trozo de círculo. Lo uso
            porque pygame.draw.arc solo dibuja el perímetro del arco y no el trozo
            completo, por lo que no lo puedo usar para dibujar el rango en forma de
            cono.
        '''

        # Obtengo el ángulo medio, el ángulo de arco de cada paso y el centro del
        # círculo
        midAngle = angle/2
        step = angle/slices
        (centerX, centerY) = center
        currentStep = -midAngle

        # Paso a calcular cada punto del arco
        listPoints = [center]
        while currentStep < midAngle:
            x = math.cos(currentStep) * radius + centerX
            y = math.sin(currentStep) * radius + centerY
            listPoints.append((x, y))
            currentStep = min(currentStep+step, midAngle)

        return listPoints

    @classmethod
    def get_angle(cls, move):
        '''
            Devuelve el ángulo dado un movimiento
        '''

        # Movimiento al este
        if move == E:
            return 0.0
        # Movimiento al noreste
        if move == NE:
            return 45.0
        # Movimiento al norte
        if move == N:
            return 90.0
        # Movimiento al noroeste
        if move == NW:
            return 135.0
        # Movimiento al oeste
        if move == W:
            return 180.0
        # Movimiento al suroeste
        if move == SW:
            return 225.0
        # Movimiento al sur
        if move == S or move == STILL:
            return 270.0
        # Movimiento al sureste
        if move == SE:
            return 315.0

    @classmethod
    def get_move(cls, angle):
        '''
            Devuelve el movimiento dado un ángulo
        '''

        # Movimiento al este
        if angle == 0:
            return E
        # Movimiento al noreste
        if angle == 45:
            return NE
        # Movimiento al norte
        if angle == 90:
            return N
        # Movimiento al noroeste
        if angle == 135:
            return NW
        # Movimiento al oeste
        if angle == 180:
            return W
        # Movimiento al suroeste
        if angle == 225:
            return SW
        # Movimiento al sur
        if angle == 270:
            return S
        # Movimiento al sureste
        if angle == 315:
            return SE

    @classmethod
    def discretice_angle(cls, angle):
        '''
            Discretiza un ángulo aleatorio dado y devuelve el ángulo
            discretizado y el movimiento asociado
        '''
        # Movimiento al este
        if angle < 22.5 or angle >= 337.5:
            return 0.0, cls.get_move(0)
        # Movimiento al noreste
        if angle >= 22.5 and angle < 67.5:
            return 45.0, cls.get_move(45)
        # Movimiento al norte
        if angle >= 67.5 and angle < 112.5:
            return 90.0, cls.get_move(90)
        # Movimiento al noroeste
        if angle >= 112.5 and angle < 157.5:
            return 135.0, cls.get_move(135)
        # Movimiento al oeste
        if angle >= 157.5 and angle < 202.5:
            return 180.0, cls.get_move(180)
        # Movimiento al suroeste
        if angle >= 202.5 and angle < 247.5:
            return 225.0, cls.get_move(225)
        # Movimiento al sur
        if angle >= 247.5 and angle < 292.5:
            return 270.0, cls.get_move(270)
        # Movimiento al sureste
        if angle >= 292.5 and angle < 337.5:
            return 315.0, cls.get_move(315)
