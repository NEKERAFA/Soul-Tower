# -*- coding: utf-8 -*-

import pygame
from src.sprites.Character import *
from src.sprites.characters.Player import *
from src.sprites.characters.player.PlayerState import *

class PlayerState(object):
	name = "state"
	def change(self, state):
		raise NotImplementedError('Error: Abstract class')

	def update_pos(self, player, mapRect, mapMask, time):
		Character.update(player, mapRect, mapMask, time)
