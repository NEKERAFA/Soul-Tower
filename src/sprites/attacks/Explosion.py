# -*- coding: utf-8 -*-

import pygame, sys, os, math, random
from src.sprites.Attack import *

# -------------------------------------------------
# Sprites de ataques
class Explosion(Attack):
    def __init__(self, position, enemies):
        # Obtenemos las rutas a los archivos
        imageFile = os.path.join('sprites', 'attacks', 'explosion.png')
        spriteSheet = os.path.join('attacks', 'explosion.json')
        self.damage = 1
        self.position = position
        x,y = position
        self.rotation = random.uniform(-180,180)

        # Invocamos al constructor de la clase padre
        Attack.__init__(self, imageFile, spriteSheet, enemies)
        self.image = pygame.transform.scale(self.origImage, (int(self.rect.width*2), int(self.rect.height*2)))
        print(self.rect.height, self.rect.width)
        self.rect.topleft = x-self.rect.height,y-self.rect.width
        # self.rect.bottomleft = x-self.rect.height/2,y-self.rect.width-16
        # self.shrink = 5
        # self.blastRect = Rect(0,0,0,0)
        
    def draw(self, surface):
        Attack.draw(self, surface)
        # pygame.draw.rect(surface, (0,0,0), self.blastRect)

    def update(self, time, stage):
        self.image = pygame.transform.scale(self.origImage, (int(self.rect.width*2), int(self.rect.height*2)))

        Attack.update(self, time)
        # Colisiones
        if self.animationFrame>3:
            for enemy in self.enemies:
                if self.rect.colliderect(enemy.rect):
                    print('Explosion hit')
                    enemy.drop.change_global_position(enemy.position)
                    stage.rooms[stage.currentRoom].drops.add(enemy.drop)
                    enemy.receive_damage(self.damage, self.rotation)
        if not self.drawAnimation:
            self.kill()
