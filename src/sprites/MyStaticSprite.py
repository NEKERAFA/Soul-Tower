# -*- coding: utf-8 -*-

import pygame

# Sprites estáticos
class MyStaticSprite(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.position = (0, 0)

    # Cambia la posición en el mundo
    def change_position(self, position):
        self.position = position
        self.rect.left = self.position[0]
        self.rect.bottom = self.position[1]

    # Incrementa la posición del sprite
    def increment_position(self, increment):
        (posX, posY) = self.position
        (incrementX, incrementY) = increment
        self.change_position((posX+incrementX, posY+incrementY))
