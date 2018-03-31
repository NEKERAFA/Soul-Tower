# -*- coding: utf-8 -*-

import pygame, sys, os, math, random
from src.sprites.Attack import *
from src.sprites.Force import *

# -------------------------------------------------
# Sprites de ataques
class Thunder(Attack):
    def __init__(self, characterPos, rotation, radius, enemies):
        # Obtenemos las rutas a los archivos
        effect_sound = 'thunder.wav'
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
        Attack.__init__(self, imageFile, spriteSheet, enemies, effect_sound)
        #print('RAYOS')
        #print(self.effect_sound.get_length())
        self.image = pygame.transform.rotate(self.origImage, 90)
        self.rect.bottomleft = x-self.rect.height/2,y-self.rect.width-36
        # self.rect.bottomleft = x-self.rect.height/2,y-self.rect.width-16
        self.shrink = 5
        # self.blastRect = Rect(0,0,0,0)
        # Diccionario de ataque-enemigos
        # (para el mismo ataque no hacer daño más de una vez al mismo enemigo)
        self.attackDict = {-1:-1}

    def draw(self, surface):
        #pygame.mixer.set_reserved(1)
        #chanel_reserved_0 = pygame.mixer.Channel(0)
        #chanel_reserved_0.play(self.effect_sound)
        Attack.draw(self, surface)
        # pygame.draw.rect(surface, (0,0,0), self.blastRect)

    def update(self, player, time, stage):
        Attack.update(self, time)
        self.image = pygame.transform.rotate(self.origImage, 90)
        # Colisiones
        if self.animationFrame>3:
            self.channel_effect.sound_update(time)
            blastRect = Rect(0,0,self.rect.height-self.shrink*2,self.rect.height-self.shrink*2)
            blastRect.left = self.rect.left + self.shrink
            blastRect.bottom = self.rect.bottom + self.rect.width - self.rect.height - self.shrink
            # self.blastRect = blastRect
            for enemy in self.enemies:
                if blastRect.colliderect(enemy.rect):
                    value = self.attackDict.get(id(enemy))
                    if (value is None or value!=self.id):
                        self.attackDict[id(enemy)] = self.id
                        print("thunder enemy ", id(enemy))
                        angle = random.uniform(0, 2*math.pi)
                        impulse = Force(angle, player.stats["backward"])
                        enemy.receive_damage('magic', player.stats["atk"], impulse)
                        if (enemy.killed):
                            del self.attackDict[id(enemy)]
        if not self.drawAnimation:
            self.kill()
