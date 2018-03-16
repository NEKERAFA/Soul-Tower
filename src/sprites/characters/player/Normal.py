# -*- coding: utf-8 -*-

import pygame
from src.sprites.characters.Player import *
from src.sprites.characters.player.PlayerState import *

class Normal(PlayerState):
	name = "normal"

	def change(self, state):
		# Debug:
		# print("Changing state from ", self.name, " to ", state.name)
		
		self.__class__ = state

	def update_pos(self, player, mapRect, mapMask, time):
		Character.update(player, mapRect, mapMask, time)

	def debug(self):
		print("PlayerState = ", self.name)