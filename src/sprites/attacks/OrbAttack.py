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
class OrbAttack(Attack):
    def __init__(self, radius, delayTime, enemies, looking):
        # Obtenemos las rutas a los archivos
        castingFile = os.path.join('attacks', 'orb.png')
        castingSheet = os.path.join('attacks', 'castingOrb.json')

        self.castingAnim = MyStaticAnimatedSprite(castingFile, castingSheet)
        self.castingAnim.animationLoop = False

        orbFile = 'orb.png'
        orbSheet = 'orb.json'
        # Invocamos al constructor de la clase padre
        Attack.__init__(self, orbFile, orbSheet, enemies)

        # Rutas de las balas
        imageFile = os.path.join('sprites', 'attacks', 'laser.png')
        spriteSheet = os.path.join('attacks', 'laser.json')

        # Cargar sheet de sprites
        sheet = ResourceManager.load_image(imageFile, -1)

        # Leer coordenadas de fichero
        data = ResourceManager.load_sprite_conf(spriteSheet)
        sheetConf = []

        # Cargamos los sprites
        for col in range(0, len(data)):
            cell = data[col]
            coords = pygame.Rect((int(cell['x']), int(cell['y'])), (int(cell['width']), int(cell['height'])))
            delay = float(cell['delay'])*1000
            sheetConf.append({'coords': coords, 'delay': delay})
        # Frame inicial
        rect = pygame.Rect(0, 0, sheetConf[0]['coords'][2], sheetConf[0]['coords'][3])
        origImage = sheet.subsurface(sheetConf[0]['coords'])
        self.bulletImage = origImage.copy()

        self.loopAnimation = True

        # Radio de acción
        self.radius = radius
        # Tiempo entre disparos
        self.delayTime = delayTime
        self.elapsedTime = 0
        # Comprueba si está atacando
        self.attacking = True
        # Grupo de disparos
        self.bullets = pygame.sprite.Group()
        # Dirección
        self.looking = looking
        # Tiempo para acabar
        self.endDelay = 0
        self.ending = False

    def start_attack(self, pos, enemyPos):
        x,y = pos
        if self.looking == E:
            x += self.rect.width/2 + 7
        else:
            x -= self.rect.width/2 - 7
        y -= self.rect.height - 10
        self.rect.topleft = x,y
        self.castingAnim.rect.topleft = x,y
        bulletX = x+15
        bulletY = y+15
        self.bulletPos = bulletX, bulletY
        (enemyX, enemyY) = enemyPos
        # Obtenemos el ángulo entre el orbe y el enemigo
        angle = int(math.degrees(math.atan2(bulletY-enemyY, enemyX-bulletX)))

        # Corrección cuando el ángulo es entre 180-360
        if angle < 0:
            angle = 360 + angle
        self.rotation = angle
        self.attacking = True

    def end_attack(self):
        # self.ending = True
        # self.endDelay = endDelay
        self.attacking = False

    def draw(self, surface):
        if not self.castingAnim.animationFinish:
            surface.blit(self.castingAnim.image, self.castingAnim.rect)
        else:
            surface.blit(self.image, self.rect)
            self.bullets.draw(surface)

    def update(self, boss, time, stage):

        # Actualizamos el ataque
        Attack.update(self, time)

        if not self.castingAnim.animationFinish:
            self.castingAnim.update(time)

        else:
            # Si ha pasado el tiempo suficiente y estamos intentando atacar
            if (self.elapsedTime > self.delayTime) and self.attacking:
                # Se crea una bala y se guarda en el grupo de balas
                bullet = Bullet(self.bulletPos, self.rotation, self.radius, self.bulletImage, 0.15)
                self.bullets.add(bullet)

                # Y reiniciar el contador
                self.elapsedTime = 0
            else:
                self.elapsedTime += time

            # Actualizamos las balas
            self.bullets.update(time, stage, self.bulletImage)

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

        if not self.attacking and len(self.bullets.sprites())==0:
            boss.attack = None
            self.kill()
