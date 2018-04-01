# -*- coding: utf-8 -*-

import pygame, sys, os, math, random
from src.ResourceManager import *
from src.sprites.Attack import *
from src.sprites.Bullet import *
from src.sprites.Force import *
from Normalize import *
from src.sprites.MyStaticAnimatedSprite import *

# W = 1
E = 2

# -------------------------------------------------
# Sprites de ataques
class SemicircleAttack(Attack):
    def __init__(self, radius, delayTime, enemies, looking):
        # Obtenemos las rutas a los archivos
        imageFile = 'semicircle.png'
        spriteSheet = 'semicircle.json'

        # Invocamos al constructor de la clase padre
        Attack.__init__(self, imageFile, spriteSheet, enemies, None) # TODO cambiar None
        self.image = pygame.transform.scale(self.origImage, (int(self.rect.width*2), int(self.rect.height*2)))
        self.loopAnimation = True

        # Radio de acción
        self.radius = radius
        # Tiempo entre disparos
        self.delayTime = delayTime
        self.elapsedTime = 0
        # Comprueba si está atacando
        self.attacking = False
        self.ended = False
        # Grupo de disparos
        self.bullets = pygame.sprite.Group()
        # Dirección
        self.looking = looking

    def start_attack(self, pos, enemyPos):
        self.pos = pos
        bulletX,bulletY = pos
        (enemyX, enemyY) = enemyPos
        # Obtenemos el ángulo entre el orbe y el enemigo
        angle = int(math.degrees(math.atan2(bulletY-enemyY, enemyX-bulletX)))

        # Corrección cuando el ángulo es entre 180-360
        if angle < 0:
            angle = 360 + angle
        self.rotation = angle
        self.attacking = True

    def end_attack(self):
        self.attacking = False
        self.ended = True

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        self.bullets.draw(surface)

    def update(self, boss, time, stage):

        # Actualizamos el ataque
        Attack.update(self, time)

        # Si ha pasado el tiempo suficiente y estamos intentando atacar
        if (self.elapsedTime > self.delayTime) and self.attacking:
            # Se crea una bala y se guarda en el grupo de balas
            bullet = Bullet(self.pos, self.rotation, self.radius, self.image, 0.15)
            self.bullets.add(bullet)

            # Y reiniciar el contador
            self.elapsedTime = 0
        else:
            self.elapsedTime += time

        # Actualizamos las balas
        self.bullets.update(time, stage, self.image)

        # Comprobamos que enemigos colisionan con que grupos
        collides = pygame.sprite.groupcollide(self.bullets, self.enemies, True, False)

        # Si hay una colisión, hacemos daño al enemigo y matamos la bala
        for bullet in collides:
            enemies = collides[bullet]
            # Cogemos el primero en hacer la colisión para que reciba daño
            enemy = enemies[0]
            enemyPos = enemy.position
            impulse = Force(bullet.rotation, boss.stats["backward"])
            enemy.receive_damage(boss.stats["atk"], impulse)

        if self.ended and len(self.bullets.sprites())==0:
            boss.attack = None
            self.kill()
