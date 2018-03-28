# -*- coding: utf-8 -*-

import math

# ------------------------------------------------------------------------------
# Esta clase representa un vector en formato polar

class Force(object):
    def __init__(self, angle, magnitude):
        self.angle = angle
        self.magnitude = magnitude
        self.decrement = magnitude/8

    def get_coordinates(self):
        '''
            Devuelve las coordenadas cartesianas del vector
        '''
        x = math.cos(self.angle)*self.magnitude
        y = math.sin(self.angle)*self.magnitude
        return (x, y)

    def substrat(self):
        '''
            Quita cierto valor del módulo, dejándolo como mínimo a 0
        '''
        self.magnitude = max(self.magnitude-self.decrement, 0)
