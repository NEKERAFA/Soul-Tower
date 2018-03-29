# -*- coding: utf-8 -*-

import pygame, sys, os, math, random
from src.sprites.Attack import *
from src.sprites.Force import *

# -------------------------------------------------
# Sprites de ataques
class Thunder(Attack):
    def __init__(self, characterPos, rotation, radius, enemies):
        # Obtenemos las rutas a los archivos
        imageFile = os.path.join('sprites', 'attacks', 'thunder.png')
        spriteSheet = os.path.join('attacks', 'thunder.json')
        self.damage = 1
        dispersion = 40
        x,y = characterPos
        offsetX = radius * math.cos(math.radians(rotation))
        offsetY = radius * math.sin(math.radians(rotation))
        x += offsetX
        y -= offsetY
        x += random.uniform(-dispersion, dispersion)
        y += random.uniform(-dispersion, dispersion)
        self.position = x,y
        self.rotation = rotation

        # Invocamos al constructor de la clase padre
        Attack.__init__(self, imageFile, spriteSheet, enemies)
        self.image = pygame.transform.rotate(self.origImage, 90)
        self.rect.bottomleft = x-self.rect.height/2,y-self.rect.width-36
        # self.rect.bottomleft = x-self.rect.height/2,y-self.rect.width-16
        self.shrink = 5
        # self.blastRect = Rect(0,0,0,0)

    def draw(self, surface):
        Attack.draw(self, surface)
        # pygame.draw.rect(surface, (0,0,0), self.blastRect)

    def update(self, player, time, stage):
        Attack.update(self, time)
        self.image = pygame.transform.rotate(self.origImage, 90)
        # Colisiones
        if self.animationFrame>3:
            blastRect = Rect(0,0,self.rect.height-self.shrink*2,self.rect.height-self.shrink*2)
            blastRect.left = self.rect.left + self.shrink
            blastRect.bottom = self.rect.bottom + self.rect.width - self.rect.height - self.shrink
            # self.blastRect = blastRect
            for enemy in self.enemies:
                if blastRect.colliderect(enemy.rect):
                    angle = random.uniform(0, 2*math.pi)
                    impulse = Force(angle, player.stats["backward"])
                    enemy.receive_damage('magic', player.stats["atk"], impulse)
        if not self.drawAnimation:
            self.kill()