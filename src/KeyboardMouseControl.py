import pygame
from ControlManager import *
from pygame.locals import *
import math as m

class KeyboardMouseControl(ControlManager):
	def __init__(self):
		self.upButton = K_w
		self.downButton = K_s
		self.leftButton = K_a
		self.rightButton = K_d

	def up(self):
		return pygame.key.get_pressed()[self.upButton]
	def down(self):
		return pygame.key.get_pressed()[self.downButton]
	def left(self):
		return pygame.key.get_pressed()[self.leftButton]
	def right(self):
		return pygame.key.get_pressed()[self.rightButton]
	def angle(self, pos):
		(player_x, player_y) = pos
		(mouse_x, mouse_y) = pygame.mouse.get_pos()
		return m.degrees(m.atan2(player_y - mouse_y, mouse_x - player_x))

	def setKeyUp(self, newKey):
		self.upButton = newKey
	def setKeyDown(self, newKey):
		self.upDown = newKey
	def setKeyLeft(self, newKey):
		self.upLeft = newKey
	def setKeyRight(self, newKey):
		self.upRight = newKey