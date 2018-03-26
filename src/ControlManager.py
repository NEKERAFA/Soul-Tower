import pygame

class ControlManager(object):
    @classmethod
    def up(cls):
        raise NotImplementedError('Error: Abstract class')

    @classmethod
    def down(cls):
        raise NotImplementedError('Error: Abstract class')

    @classmethod
    def left(cls):
        raise NotImplementedError('Error: Abstract class')

    @classmethod
    def right(cls):
        raise NotImplementedError('Error: Abstract class')

    @classmethod
    def angle(cls, pos):
        raise NotImplementedError('Error: Abstract class')

    @classmethod
    def prim_button(cls):
        raise NotImplementedError('Error: Abstract class')

    @classmethod
    def sec_button(cls):
        raise NotImplementedError('Error: Abstract class')

    @classmethod
    def select_button(cls):
        raise NotImplementedError('Error: Abstract class')
