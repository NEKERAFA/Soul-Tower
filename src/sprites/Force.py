# -*- coding: utf-8 -*-

import math

# ------------------------------------------------------------------------------
# Esta clase representa un vector en formato polar

class Force(object):
    def __init__(self, angle, module):
        self.angle = angle
        self.module = module

    def get_coordinates(self):
        '''
            Devuelve las coordenadas cartesianas del vector
        '''
        x = math.cos(self.angle)*self.module
        y = math.sin(self.angle)*self.module
        return (x, y)

    def substrat(self, value):
        '''
            Quita cierto valor del módulo, dejándolo como mínimo a 0
        '''
        self.module = max(self.module-value, 0)
