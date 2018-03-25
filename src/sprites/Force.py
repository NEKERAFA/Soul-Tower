# -*- coding: utf-8 -*-

import math

# ------------------------------------------------------------------------------
# Esta clase representa un vector en formato polar

class Force(object):
    def __init__(self, angle, magnitude):
        self.angle = angle
        self.magnitude = magnitude

    def get_coordinates(self):
        '''
            Devuelve las coordenadas cartesianas del vector
        '''
<<<<<<< HEAD
        x = math.cos(self.angle)*self.modulo
        y = math.sin(self.angle)*self.modulo
=======
        x = math.cos(self.angle)*self.magnitude
        y = math.sin(self.angle)*self.magnitude
>>>>>>> refs/remotes/origin/master
        return (x, y)

    def substrat(self, value):
        '''
            Quita cierto valor del módulo, dejándolo como mínimo a 0
        '''
        self.magnitude = max(self.magnitude-value, 0)
