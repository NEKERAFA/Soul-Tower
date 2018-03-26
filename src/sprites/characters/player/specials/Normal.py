# -*- coding: utf-8 -*-

import pygame
from src.sprites.characters.Player import *
from src.sprites.characters.player.specials.PlayerState import *

class Normal(PlayerState):
	name = "normal"
	maxEnergy = 5 # TODO: habría que guardar el valor del json
	energyReg = 0.001 # in energy/ms
	lastDash = 0 # Tiempo transcurrido desde que finalizó el último dash

	def change(self, player, state):
		# Debug:
		# print("Changing state from ", self.name, " to ", state.name)
		if (state.name == "dashing"):
			# Si se quiere cambiar al estado dashing
			# se comprueba el tiempo transcurrido y la energía
			if (self.lastDash > 250 and player.stats["nrg"] > 2):
				player.stats["nrg"] -= 2
				self.__class__ = state
			else:
				return
		else:
			self.__class__ = state

	def update_state(self, player, time, mapRect, mapMask):
		# Se actualiza el tiempo transcurrido desde que acabó el último dash
		self.lastDash += time
		# Regeneración de energía
		player.stats["nrg"] += time*self.energyReg
		if (player.stats["nrg"]>self.maxEnergy):
			player.stats["nrg"] = self.maxEnergy

		Character.update(player, time, mapRect, mapMask)

	def debug(self):
		print("PlayerState = ", self.name)
