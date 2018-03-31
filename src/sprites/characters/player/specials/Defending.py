# -*- coding: utf-8 -*-

import pygame
from src.sprites.characters.Player import *
from src.sprites.characters.player.specials.PlayerState import *
from src.sprites.characters.player.specials.Stunned import *
from src.sprites.ShieldSprite import *

class Defending(PlayerState):
    name = "defending"
    defendCost = 2 # Energía que cuesta cada bloqueo

    def change(self, player, state):
        # Debug:
        # print("Changing state from ", self.name, " to ", state.name)
        if (state != Defending):
            player.usingShield = False
        self.__class__ = state

    def update_state(self, player, time, mapRect, mapMask):
        # self.debug()
        # Se controla el tiempo de invencibilidad (método heredado)
        self.update_inv_time(time)
        player.set_energy(min(player.stats["max_nrg"], player.stats["nrg"] + time*player.stats["nrg_reg_bck"]))
        Character.update_movement(player, time)
        speedX, speedY = player.speed
        player.speed = (speedX*0.3,speedY*0.3)
        MySprite.update(player, time)
        Character.fix_collision(player, mapMask)
        player.usingShield = True
        x,y = player.position
        x += player.rect.width/4
        y -= player.rect.height/8
        player.shield.change_position((x,y))

    def receive_damage_aux(self, player, damage, force):
        # Si no tiene suficiente energía, entrar en estado de "stun"
        if (player.stats["nrg"]-self.defendCost<0):
            print("Energía insuficiente. Jugador aturdido")
            #player.stats["nrg"] = 0
            player.set_energy(0)
            self.change(player, Stunned)
            player.state.receive_damage(player, damage, force)
        else:
            player.add_energy(-self.defendCost)
            print("Daño defendido")

    def debug(self):
        print("PlayerState = ", self.name)
