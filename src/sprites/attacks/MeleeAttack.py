# -*- coding: utf-8 -*-

import pygame, sys, os, math, random
from src.sprites.Attack import *
from src.sprites.attacks.Thunder import *
from src.sprites.Force import *
from src.sprites.attacks.Explosion import *

# -------------------------------------------------
# Sprites de ataques
class MeleeAttack(Attack):
    def __init__(self, radius, delayTime, enemies):
        # Obtenemos las rutas a los archivos
        imageFile = os.path.join('sprites', 'attacks', 'melee.png')
        spriteSheet = os.path.join('attacks', 'melee.json')

        # Invocamos al constructor de la clase padre
        Attack.__init__(self, imageFile, spriteSheet, enemies)

        # Tiempo entre ataques melee
        self.delayTime = delayTime
        self.elapsedTime = 0
        # Radio del ataque
        self.radius = radius
        # Comprueba si está atacando
        self.attacking = False
        # Grupo de rayos
        self.thunders = pygame.sprite.Group()
        # Grupo de explosiones
        self.explosions = pygame.sprite.Group()
        # Nivel de mejora
        self.level = 3
        self.probLvl2 = 0.7
        self.probLvl3 = 0.45
        # Diccionario de ataque-enemigos
        # (para el mismo ataque no hacer daño más de una vez al mismo enemigo)
        self.attackDict = {-1:-1}

    def draw(self, surface):
        Attack.draw(self, surface)
        for thunder in self.thunders:
            thunder.draw(surface)
        for explosion in self.explosions:
            explosion.draw(surface)

    def start_attack(self, characterPos, rotation):
        self.attacking = True
        self.position = Attack.calc_rot_pos(rotation, self.radius, self.rect.width, self.rect.height, characterPos)
        self.rect.left = self.position[0]
        self.rect.top = self.position[1]
        self.rotation = rotation
        self.characterPos = characterPos

    def end_attack(self):
        self.attacking = False

    def update(self, player, time, stage):
        # Si ha pasado el tiempo suficiente y estamos intentando atacar
        if (self.elapsedTime > self.delayTime) and self.attacking:
            self.drawAnimation = True
            # Y reiniciar el contador
            self.elapsedTime = 0
            # Si tenemos nivel suficiente
            if (self.level>2 and random.random()<=self.probLvl3):
                thunder = Thunder(self.characterPos, self.rotation, self.radius+30, self.enemies)
                self.thunders.add(thunder)
        else:
            self.elapsedTime += time

        Attack.update(self, time)

        if self.drawAnimation:
            if self.rotation >= 90:
                self.image = pygame.transform.rotate(self.origImage, 180-self.rotation)
                self.image = pygame.transform.flip(self.image, True, False)
            elif self.rotation <= -90:
                self.image = pygame.transform.rotate(self.origImage, -180-self.rotation)
                self.image = pygame.transform.flip(self.image, True, False)
            else:
                self.image = pygame.transform.rotate(self.origImage, self.rotation)

            # Colisiones
            for enemy in self.enemies:
                (atkX, atkY) = self.position
                (enemyX, enemyY) = enemy.position
                # atkY -= self.image.get_height()
                enemyY -= enemy.image.get_height()
                offset = (int(enemyX - atkX), int(enemyY - atkY))
                self.mask = pygame.mask.from_surface(self.image)
                collision = self.mask.overlap(enemy.mask, offset)
                if collision is not None:
                    # Comprobamos si aun no hemos dañado al enemigo
                    value = self.attackDict.get(id(enemy))
                    if (value is None or value!=self.id):
                        self.attackDict[id(enemy)] = self.id
                        enemyPos = enemy.rect.center
                        impulse = Force(self.rotation, player.stats["backward"])
                        enemy.receive_damage('physic', player.stats["atk"], impulse)
                        if (self.level>1 and enemy.justDied and random.random()<=self.probLvl2):
                            explosion = Explosion(enemyPos, self.enemies)
                            self.explosions.add(explosion)
                            del self.attackDict[id(enemy)]
                        impulse = Force(self.rotation, player.stats["backward"])
                        enemy.receive_damage('physic', player.stats["atk"], impulse)

        self.thunders.update(player, time, stage)
        self.explosions.update(player, time, stage)
<<<<<<< HEAD
            # Comprobamos que enemigos colisionan con que grupos
            # enemiesCollide = pygame.sprite.spritecollide(self, self.enemies, False, pygame.sprite.collide_mask)

        self.thunders.update(player, time, stage)
        self.explosions.update(player, time, stage)
=======
>>>>>>> b6b8678d9689066f852a6cfd7544a0e36d5010bd
