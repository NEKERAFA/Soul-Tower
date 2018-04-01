# -*- coding: utf-8 -*-

import pygame
from src.sprites.Character import *
from src.sprites.characters.Player import *

class PlayerState(object):
    name = "state"
    invTime = 500 # Tiempo de invencibilidad después de recibir daño (ms)
    invElapsed = 0 # Tiempo desde que se ha activado la invencibilidad (ms)
    invEnabled = False # Estado de invencibilidad sí/no

    def change(self, player, state):
        raise NotImplementedError('Error: Abstract class')

    def update_state(self, player, time, mapRect, mapMask):
        Character.update(player, time, mapRect, mapMask)

    def receive_damage(self, player, damage, force):
        # Se actualiza el estado de invencibilidad
        # y se comprueba si toca recibir daño
        damage = self.update_inv()
        if damage:
            self.receive_damage_aux(player, damage, force)

    def receive_damage_aux(self, player, damage, force):
        player.channel_damage.play(player.damage_sound)
        Character.receive_damage(player, damage, force)

    def update_inv_time(self, time):
        if self.invEnabled:
            self.invElapsed += time

    def update_inv(self):
        # si eres invencible
        if self.invEnabled:
            if self.invElapsed >= self.invTime:
            # si ha pasado el tiempo suficiente
                self.invEnabled = False
                # dejas de serlo
            # no recibes daño esta vez
            return False
        # si no
        else:
            # te vuelves invencible
            self.invEnabled = True
            # pones el timpo a 0
            self.invElapsed = 0
            # recibes daño
            return True
