# -*- coding: utf-8 -*-

from src.sprites.Character import *

# ------------------------------------------------------------------------------
# Clase BehaviourState

class BehaviourState(object):
    def move_ai(self, enemy, player):
        raise NotImplemented("Tiene que implementar el metodo move_ai.")

    def update(self, enemy, time, mapRect, mapMask):
        raise NotImplemented("Tiene que implementar el metodo update")

    def receive_damage(self, enemy, attack, damage, force):
        if attack == 'melee':
            damage = max(damage-enemy.stats["phy_def"], 0)
        elif attack == 'ranged':
            damage = max(damage-enemy.stats["mag_def"], 0)

        Character.receive_damage(enemy, damage, force)
