# -*- coding: utf-8 -*-

import pygame, math
from src.ResourceManager import *
from src.sprites.MyStaticSprite import *

# -------------------------------------------------
# Clase EnemyRange

class EnemyRange(MyStaticSprite):
    '''
        radius: int, Radio de visión
        angle: float, Ángulo de visión
        lookAt: int, Ángulo hacia donde mira al iniciarse
    '''
    def __init__(self, radius, angle, lookAt):
        # Llamamos al constructor de la superclase
        MyStaticSprite.__init__(self)
        # Guardo el radio y el ángulo de vision
        self.radius = radius
        self.angle = angle
        # Creamos la imagen para hacer el mapa y la pintamos de negro
        self.image = pygame.Surface((radius*2, radius*2))
        # Establecemos el rectángulo
        self.rect = self.image.get_rect()
        # Obtengo los puntos del polígono
        arc = get_slice_circle((radius, radius), radius, angle, math.pi/32)
        # Dibujo el arco que actuará como campo de visión
        pygame.draw.polygon(self.image, (255, 255, 255), arc)
        # Convierto lo negro a transparente
        self.image.set_colorkey((0, 0, 0))
        # Creo la máscara
        EnemyRange.look_at(self, lookAt)
        self.lookAt = lookAt

    def look_at(self, angle):
        self.lookAt = angle
        center = self.rect.center
        # Roto la imagen para cargarla como máscara
        rotImage = pygame.transform.rotate(self.image, self.lookAt)
        self.rect = rotImage.get_rect()
        self.rect.center = center
        # Creo la máscara con la imagen rotada
        self.mask = pygame.mask.from_surface(rotImage)

def get_slice_circle(center, radius, angle, step):
    '''
        Obtiene una lista de puntos que representan un trozo de círculo. Lo uso
        porque pygame.draw.arc solo dibuja el perímetro del arco y no el trozo
        completo, por lo que no lo puedo usar para dibujar el rango en forma de
        cono.
    '''

    # Obtengo el ángulo medio, el paso actual y el centro del círculo
    midAngle = angle/2
    currentStep = -midAngle
    (centerX, centerY) = center

    # Paso a calcular cada punto del arco
    listPoints = [center]
    while currentStep < midAngle:
        x = math.cos(currentStep) * radius + centerX
        y = math.sin(currentStep) * radius + centerY
        listPoints.append((x, y))
        currentStep = min(currentStep+step, midAngle)

    return listPoints
