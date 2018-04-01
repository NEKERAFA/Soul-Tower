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
class DeathSlashAttack(Attack):
    def __init__(self, enemies, looking):
        # Obtenemos las rutas a los archivos

        imageFile = 'death_slash.png'
        spriteSheet = 'death_slash.json'
        effect_sound = 'slash.ogg'

        # Invocamos al constructor de la clase padre
        Attack.__init__(self, imageFile, spriteSheet, enemies, effect_sound)

        # Dirección
        self.looking = looking
        self.attacking = True

    def start_attack(self, topLeft, angle):
        x,y = topLeft
        if self.looking == E:
            x -= 21
        else:
            x -= 69
        y -= 3
        self.rect.topleft = x,y
        self.angle = angle


    def end_attack(self):
        # self.ending = True
        # self.endDelay = endDelay
        self.attacking = False

    def draw(self, surface):
        if self.looking == E:
            image = pygame.transform.flip(self.image, 1, 0)
        else:
            image = self.image
        surface.blit(image, self.rect)

    def update(self, boss, time, stage):

        # Actualizamos el ataque
        Attack.update(self, time)


        # Colisiones
        for enemy in iter(self.enemies):
            (atkX, atkY) = self.rect.topleft
            (enemyX, enemyY) = enemy.position
            # print(self.rect.topleft, enemy.position)
            # atkY -= self.image.get_height()
            enemyY -= enemy.image.get_height()
            offset = (int(enemyX - atkX), int(enemyY - atkY))
            if self.looking == E:
                image = pygame.transform.flip(self.image, 1, 0)
            else:
                image = self.image
            self.mask = pygame.mask.from_surface(image)
            collision = self.mask.overlap(enemy.mask, offset)
            if collision is not None:
                impulse = Force(self.angle, boss.stats["backward"])
                enemy.receive_damage(boss.stats["atk"], impulse)
            # # Comprobamos que enemigos colisionan con que grupos
            # collides = pygame.sprite.groupcollide(self.bullets, self.enemies, True, False)

            # # Si hay una colisión, hacemos daño al enemigo y matamos la bala
            # for bullet in collides:
            #     enemies = collides[bullet]
            #     # Cogemos el primero en hacer la colisión para que reciba daño
            #     enemy = enemies[0]
            #     enemyPos = enemy.position
            #     impulse = Force(bullet.rotation, boss.stats["backward"])
            #     enemy.receive_damage(boss.stats["atk"], impulse)

        # if not self.attacking and len(self.bullets.sprites())==0:
        #     print("killing attck")
        #     boss.attack = None
        #     self.kill()
        if not self.attacking:
            boss.attack = None
            self.kill() # TODO: creo que no hace falta
