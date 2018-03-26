# -*- coding: utf-8 -*-

import pygame
from src.sprites.Character import *
from src.sprites.characters.Player import *

class PlayerState(object):
	name = "state"
	def change(self, player, state):
		raise NotImplementedError('Error: Abstract class')

	def update_state(self, player, mapRect, mapMask, time):
		Character.update(player, mapRect, mapMask, time)
