# -*- coding: utf-8 -*-

import pygame, math, os
from src.sprites.Character import *
from src.sprites.EnemyRange import *
from src.sprites.Force import *
from src.sprites.characters.NPC import *
from src.sprites.characters.behaviours.BehaviourConstructor import *
from src.ResourceManager import *

ENEMY_PATH = 'enemies'

class Enemy(NPC):
    def __init__(self, spriteName, drop):
        path = os.path.join(ENEMY_PATH, spriteName)

        NPC.__init__(self, path + '.png', path + '.json')
        self.drop = drop
        self.state = BehaviourConstructor.get_behaviour(self.behaviour["type"], self)
        self.wasAlive = True
        self.justDied = False
        self.attack = None

    def move_ai(self, player):
        self.state.move_ai(self, player)

        # Comprobamos que el enemigo esté golpeando al jugador
        if pygame.sprite.collide_mask(player, self):
            angle = math.radians(360-EnemyRange.get_angle(self.movement))
            impulse = Force(angle, self.stats["backward"])
            player.receive_damage(self.stats["atk"], impulse)

    def receive_damage(self, attack, damage, force):
        self.state.receive_damage(self, attack, damage, force)
        if self.killed and self.wasAlive:
            self.justDied = True
            self.wasAlive = False
        else:
            self.justDied = False

    def update(self, time, mapRect, stage):
        self.state.update(self, time, mapRect, stage.mask)
        if (self.attack is not None):
            self.attack.update(self, time, stage)

    def draw(self, screen):
        # Esta función está para agrupar el mostrar al enemigo y su ataque
        screen.blit(self.image, self.rect)
        if (self.attack is not None):
            # print("drawing enemy attack")
            self.attack.draw(screen)

    def set_drop(self, dropGroup):
        self.drop.change_position(self.rect.midbottom)
        dropGroup.add(self.drop)

    def change_behaviour(self, behaviour):
        self.state = behaviour
