# -*- coding: utf-8 -*-

import pygame, os
from src.ResourceManager import *
from src.sprites.Drop import *

# -------------------------------------------------
# Clase Life

class Life(Drop):
    def __init__(self, amount):
        # Primero invocamos al constructor de la clase padre
        Drop.__init__(self, 'heart', amount)
