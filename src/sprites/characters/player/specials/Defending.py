# -*- coding: utf-8 -*-

import pygame
from src.sprites.characters.Player import *
from src.sprites.characters.player.specials.PlayerState import *
from src.sprites.characters.player.specials.Stunned import *

class Defending(PlayerState):
    name = "defending"
    defendCost = 2 # Energía que cuesta cada bloqueo

    def change(self, player, state):
        # Debug:
        # print("Changing state from ", self.name, " to ", state.name)
        self.__class__ = state

    def update_state(self, player, time, mapRect, mapMask):
        # self.debug()
        # Se controla el tiempo de invencibilidad (método heredado)
        self.update_inv_time(time)
        # Regeneración de energía reducida por bloqueo
        player.stats["nrg"] += time*player.stats["nrg_reg_bck"]
        # Establecer tope
        player.stats["nrg"] = min(player.stats["max_nrg"], player.stats["nrg"])
        Character.update_movement(player, time)
        speedX, speedY = player.speed
        player.speed = (speedX*0.3,speedY*0.3)
        MySprite.update(player, time)
        Character.fix_collision(player, mapMask)

    def receive_damage_aux(self, player, damage, force):
        # TODO: si no tiene suficiente energía, entrar en estado de "stun"
        player.stats["nrg"] -= self.defendCost
        if (player.stats["nrg"]<0):
            print("Energía insuficiente. Jugador aturdido")
            player.stats["nrg"] = 0
            self.change(player, Stunned)
            player.state.receive_damage(player, damage, force)
        else:
            print("Daño defendido")

    def debug(self):
        print("PlayerState = ", self.name)
