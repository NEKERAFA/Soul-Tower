# -*- coding: utf-8 -*-

import pygame, math, os
from src.sprites.Character import *
from src.sprites.EnemyRange import *
from src.sprites.Force import *
from src.sprites.characters.NPC import *
from src.sprites.behaviours.BehaviourConstructor import *
from src.ResourceManager import *

ENEMY_PATH = 'enemies'

class Enemy(NPC):
    def __init__(self, spriteName, drop):
        path = os.path.join(ENEMY_PATH, spriteName)

        NPC.__init__(self, path + '.png', path + '.json')
        self.drop = drop
        self.state = BehaviourConstructor.get_behaviour(self.behaviour["type"], self)

    def move_ai(self, player):
        self.state.move_ai(self, player)

        # Comprobamos que el enemigo no esté golpeando al jugador
        if pygame.sprite.collide_rect(player, self):
            angle = math.radians(360-EnemyRange.get_angle(self.movement))
            impulse = Force(angle, self.stats["backward"])
            player.receive_damage(self.stats["atk"], impulse)

    def update(self, time, mapRect, mapMask):
        self.state.update(self, time, mapRect, mapMask)

    def set_drop(self, dropGroup):
        self.drop.change_position(self.rect.midbottom)
        dropGroup.add(self.drop)
