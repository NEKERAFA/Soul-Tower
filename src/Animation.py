# -*- encoding: utf-8 -*-

import lib.pyganim

# -------------------------------------------------
# Clase Animacion

# Extendemos la clase animacion de PygAnimation para darle posicion
class Animation(pyganim.PygAnimation):
    def __init__(self, *args):
        pyganim.PygAnimation.__init__(self, args)
        # Posicion que tendra esta animacion
        self.position = (0, 0)

    def move(self, increment):
        (incX, incY) = increment
        (posX, posY) = self.position
        self.posicion = (posX+incX, posY+incY)

    def draw(self, screen):
        self.blit(screen, self.position)
