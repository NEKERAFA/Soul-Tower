import pygame

class ControlManager(object):
	def up(self):
		raise NotImplementedError('Error: Abstract class')
	def down(self):
		raise NotImplementedError('Error: Abstract class')
	def left(self):
		raise NotImplementedError('Error: Abstract class')
	def right(self):
		raise NotImplementedError('Error: Abstract class')
	def angle(self, pos):
		raise NotImplementedError('Error: Abstract class')
