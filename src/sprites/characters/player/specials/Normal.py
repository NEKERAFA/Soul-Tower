# -*- coding: utf-8 -*-

import pygame
from src.sprites.characters.Player import *
from src.sprites.characters.player.specials.PlayerState import *

class Normal(PlayerState):
	name = "normal"
	lastDash = 0 # Tiempo transcurrido desde que finalizó el último dash
	timeToDash = 250 # Tiempo que debe transcurrir para volver a dashear
	dashCost = 2 # Energía que cuesta cada dash

	def change(self, player, state):
		# Debug:
		# print("Changing state from ", self.name, " to ", state.name)
		if (state.name == "dashing"):
			# Si se quiere cambiar al estado dashing
			# se comprueba el tiempo transcurrido y la energía
			if (self.lastDash > self.timeToDash and player.stats["nrg"] > 2):
				player.stats["nrg"] -= self.dashCost
				self.__class__ = state
			else:
				return
		else:
			self.__class__ = state

	def update_state(self, player, time, mapRect, mapMask):
		# self.debug()
		# Se controla el tiempo de invencibilidad (método heredado)
		self.update_inv_time(time)
		# Se actualiza el tiempo transcurrido desde que acabó el último dash
		self.lastDash += time
		# Regeneración de energía
		player.stats["nrg"] += time*player.stats["nrg_reg"]
		# Establecer tope
		player.stats["nrg"] = min(player.stats["max_nrg"], player.stats["nrg"])
		Character.update(player, time, mapRect, mapMask)

	def debug(self):
		print("PlayerState = ", self.name)
