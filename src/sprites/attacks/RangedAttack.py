# -*- coding: utf-8 -*-

import pygame, sys, os, math, random
from src.sprites.Attack import *
from src.sprites.Bullet import *
from src.sprites.Force import *
from Normalize import *

# -------------------------------------------------
# Sprites de ataques
class RangedAttack(Attack):
    def __init__(self, radius, delayTime, level, enemies):
        # Obtenemos las rutas a los archivos
        imageFile = 'ranged.png'
        spriteSheet = 'ranged.json'
        effect_sound = 'pew.ogg'

        # Invocamos al constructor de la clase padre
        Attack.__init__(self, imageFile, spriteSheet, enemies, effect_sound)
        self.loopAnimation = True

        # Radio de acción
        self.radius = radius
        # Grupo de enemigos
        # self.enemies = enemies
        # Tiempo entre disparos
        self.delayTime = delayTime
        self.elapsedTime = self.delayTime
        # Comprueba si está atacando
        self.attacking = False
        # Grupo de disparos
        self.bullets = pygame.sprite.Group()
        # Nivel de mejora
        self.level = level
        self.probLvl2 = 0.7
        self.probLvl3 = 0.5


    def start_attack(self, characterPos, rotation):
        self.characterPos = characterPos
        self.rotation = rotation
        self.attacking = True

    def end_attack(self):
        self.attacking = False

    def draw(self, surface):
        self.bullets.draw(surface)

    def update(self, player, time, stage):
        # Actualizamos el ataque
        Attack.update(self, time)

        # Si ha pasado el tiempo suficiente y estamos intentando atacar
        if (self.elapsedTime >= self.delayTime) and self.attacking:
            #Se llama a la funcion sound_update del channel_effect
            self.channel_effect.soundUpdate(time)
            # Se crea una bala y se guarda en el grupo de balas
            bullet = Bullet(self.characterPos, self.rotation, self.radius, self.image)
            self.bullets.add(bullet)
            # Si tenemos nivel suficiente, se pueden lanzar dos extra
            if (self.level>2 and random.random()<=self.probLvl3):
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
        self.bullets.update(time, stage, self.image)

        # Comprobamos que enemigos colisionan con que grupos
        # collides = pygame.sprite.groupcollide(self.bullets, self.enemies, True, False)

        # # Si hay una colisión, hacemos daño al enemigo y matamos la bala
        # for bullet in collides:
        #     enemies = collides[bullet]
        #     # Cogemos el primero en hacer la colisión para que reciba daño
        #     enemy = enemies[0]
        #     enemyPos = enemy.position
        #     impulse = Force(bullet.rotation, player.stats["backward"])
        #     enemy.receive_damage('magic', player.stats["atk"], impulse)
        #     if (self.level>1 and enemy.justDied and random.random()<=self.probLvl2):
        #         # enemy.kill()
        #         angle = random.uniform(-180,180)
        #         bulletExtra = Bullet(enemyPos, angle, self.radius, self.image)
        #         self.bullets.add(bulletExtra)

        for bullet in iter(self.bullets):
            for enemy in iter(self.enemies):
                (atkX, atkY) = bullet.position
                (enemyX, enemyY) = enemy.position
                # atkY -= self.image.get_height()
                enemyY -= enemy.image.get_height()/2
                offset = (int(enemyX - atkX), int(enemyY - atkY))
                self.mask = pygame.mask.from_surface(self.image)
                collision = self.mask.overlap(enemy.mask, offset)
                if collision is not None:
                    impulse = Force(bullet.rotation, player.stats["backward"])
                    enemy.receive_damage('magic', player.stats["atk"], impulse)
                    bullet.kill()
                    if (self.level>1 and enemy.justDied and random.random()<=self.probLvl2):
                        # enemy.kill()
                        angle = random.uniform(-180,180)
                        bulletExtra = Bullet(enemy.position, angle, self.radius, self.image)
                        self.bullets.add(bulletExtra)
