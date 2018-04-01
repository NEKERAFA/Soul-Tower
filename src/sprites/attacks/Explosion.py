# -*- coding: utf-8 -*-

import pygame, sys, os, math, random
from src.sprites.Attack import *
from src.sprites.Force import *

# -------------------------------------------------
# Sprites de ataques
class Explosion(Attack):
    def __init__(self, position, enemies):
        # Obtenemos las rutas a los archivos
<<<<<<< HEAD
        imageFile = 'explosion.png'
        spriteSheet = 'explosion.json'
        effect_sound = 'explosion.wav'
=======
        effect_sound = 'explosion.ogg'
        imageFile = os.path.join('sprites', 'attacks', 'explosion.png')
        spriteSheet = os.path.join('attacks', 'explosion.json')
>>>>>>> origin/animations_sound
        self.damage = 1
        self.position = position
        x,y = position
        self.rotation = random.uniform(-180,180)

        # Invocamos al constructor de la clase padre
        Attack.__init__(self, imageFile, spriteSheet, enemies, effect_sound)
        self.image = pygame.transform.scale(self.origImage, (int(self.rect.width*2), int(self.rect.height*2)))
        # print(self.rect.height, self.rect.width)
        self.rect.topleft = x-self.rect.height,y-self.rect.width
        # self.rect.bottomleft = x-self.rect.height/2,y-self.rect.width-16
        # self.shrink = 5
        # self.blastRect = Rect(0,0,0,0)
        # Diccionario de ataque-enemigos
        # (para el mismo ataque no hacer daño más de una vez al mismo enemigo)
        self.attackDict = {-1:-1}

    def draw(self, surface):
        pygame.mixer.set_reserved(1)
        chanel_reserved_0 = pygame.mixer.Channel(0)
        chanel_reserved_0.play(self.effect_sound)
        Attack.draw(self, surface)
        # pygame.draw.rect(surface, (0,0,0), self.blastRect)

    def update(self, player, time, stage):
        self.image = pygame.transform.scale(self.origImage, (int(self.rect.width*2), int(self.rect.height*2)))

        Attack.update(self, time)
        # Colisiones
        if self.animationFrame>3:
            self.channel_effect.soundUpdate(time)
            for enemy in self.enemies:
                if self.rect.colliderect(enemy.rect):
                    value = self.attackDict.get(id(enemy))
                    if (value is None or value!=self.id):
                        self.attackDict[id(enemy)] = self.id
                        angle = random.uniform(0, 2*math.pi)
                        impulse = Force(angle, player.stats["backward"])
                        enemy.receive_damage('physic', player.stats["atk"], impulse)
                        if (enemy.killed):
                            del self.attackDict[id(enemy)]
        if not self.drawAnimation:
            self.kill()
