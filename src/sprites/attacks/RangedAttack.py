# -*- coding: utf-8 -*-

import pygame, sys, os, math, random
from src.sprites.Attack import *
from src.sprites.Bullet import *
from Normalize import *

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
        # Nivel de mejora
        self.level = 2
        self.probability = 0.3

    def start_attack(self, characterPos, rotation):
        self.characterPos = characterPos
        self.rotation = rotation
        self.attacking = True

    def end_attack(self):
        self.attacking = False

    def draw(self, surface):
        self.bullets.draw(surface)

    def update(self, time, stage):
        # Actualizamos el ataque
        Attack.update(self, time)

        # Si ha pasado el tiempo suficiente y estamos intentando atacar
        if (self.elapsedTime > self.delayTime) and self.attacking:
            # Se crea una bala y se guarda en el grupo de balas
            bullet = Bullet(self.characterPos, self.rotation, self.radius, self.image)
            self.bullets.add(bullet)
            # Si tenemos nivel suficiente, se pueden lanzar dos extra
            if (self.level>1 and random.random()<=self.probability):
                rot2 = normalize(self.rotation + 15, -180, 180)
                rot3 = normalize(self.rotation - 15, -180, 180)
                bullet2 = Bullet(self.characterPos, rot2, self.radius, self.image)
                bullet3 = Bullet(self.characterPos, rot3, self.radius, self.image)
                self.bullets.add(bullet2)
                self.bullets.add(bullet3)

            # Y reiniciar el contador
            self.elapsedTime = 0
        else:
            self.elapsedTime += time

        # Actualizamos las balas
        self.bullets.update(time, stage.mask, self.image)

        # Comprobamos que enemigos colisionan con que grupos
        for bullet in iter(self.bullets):
            enemyCollide = pygame.sprite.spritecollideany(bullet, self.enemies)

            # Si hay una colisión, hacemos daño al jugador y matamos la bala
            if enemyCollide is not None:
                enemyCollide.drop.change_global_position(enemyCollide.position)
                stage.rooms[stage.currentRoom].drops.add(enemyCollide.drop)
                enemyCollide.receive_damage(1, bullet.rotation)
