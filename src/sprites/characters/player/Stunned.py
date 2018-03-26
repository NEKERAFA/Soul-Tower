# -*- coding: utf-8 -*-

import pygame
from src.sprites.characters.Player import *
from src.sprites.characters.player.PlayerState import *

class Stunned(PlayerState):
    name = "stunned"
    stunTime = 1000 # Duración del aturdido en ms
    stunnedTime = 0 # Tiempo que lleva aturdido
    stunned = True

    def change(self, player, state):
        # Debug:
        # print("Changing state from ", self.name, " to ", state.name)
        if not self.stunned:
            self.__class__ = state

    def update_state(self, player, time, mapRect, mapMask):
        # self.debug()
        # Se controla el tiempo de invencibilidad (método heredado)
        self.update_inv_time(time)
        # Se actualiza el tiempo transcurrido desde que está aturdido
        self.stunnedTime += time
        # Si ha pasado el tiempo suficiente
        if (self.stunnedTime >= self.stunTime):
            # Se reinician los valores
            self.stunned = False
            self.stunnedTime = 0
            self.change(player, Normal)
        else:
            self.stunned = True
        # Regeneración de energía
        player.stats["nrg"] += time*player.stats["nrg_reg"]
        # Establecer tope
        player.stats["nrg"] = min(player.stats["max_nrg"], player.stats["nrg"])
        # No te puedes mover
        #Character.update(player, time, mapRect, mapMask)

    def debug(self):
        print("PlayerState = ", self.name)