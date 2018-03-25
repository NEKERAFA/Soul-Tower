# -*- coding: utf-8 -*-

import pygame, sys, os, math
from src.sprites.Attack import *
from src.sprites.Bullet import *

# -------------------------------------------------
# Sprites de ataques
class RangedAttack(Attack):
    def __init__(self, radius, delayTime, enemies):
        # Obtenemos las rutas a los archivos
        imageFile = os.path.join('sprites', 'attacks', 'ranged.png')
        spriteSheet = os.path.join('attacks', 'ranged.json')

        # Invocamos al constructor de la clase padre
        Attack.__init__(self, imageFile, spriteSheet, enemies)
        self.loopAnimation = True

        # Radio de acción
        self.radius = radius
        # Grupo de enemigos
        self.enemies = enemies
        # Tiempo entre disparos
        self.delayTime = delayTime
        self.elapsedTime = 0
        # Comprueba si está atacando
        self.attacking = False
        # Grupo de disparos
        self.bullets = pygame.sprite.Group()

    def start_attack(self, characterPos, rotation):
        self.characterPos = characterPos
        self.rotation = rotation
        self.attacking = True

    def end_attack(self):
        self.attacking = False

    def draw(self, surface):
        self.bullets.draw(surface)

    def update(self, time, mapMask):
        # Actualizamos el ataque
        Attack.update(self, time)

        # Si ha pasado el tiempo suficiente y estamos intentando atacar
        if (self.elapsedTime > self.delayTime) and self.attacking:
            # Se crea una bala y se guarda en el grupo de balas
            bullet = Bullet(self.characterPos, self.rotation, self.radius, self.image, self.rect)
            self.bullets.add(bullet)
            # Y reiniciar el contador
            self.elapsedTime = 0
        else:
            self.elapsedTime += time

        # Actualizamos las balas
        self.bullets.update(time, mapMask, self.image, self.mask, self.rect)

        # TODO: Comprobar colisión con enemigos
