# -*- coding: utf-8 -*-

from src.sprites.MyStaticSprite import *
from src.ResourceManager import *
import pygame, os

DOORS_PATH = 'doors'

class Door(MyStaticSprite):
    def __init__(self, position, imagePath, stageMask):
        MyStaticSprite.__init__(self)

        self.image = ResourceManager.load_image(os.path.join(DOORS_PATH, imagePath))
        self.rect = self.image.get_rect()
        self.change_position(position)
        self.mask = pygame.mask.from_surface(self.image)
        (posX, posY) = position
        posY = posY - self.rect.height
        self.offset = (posX, posY)
        stageMask.draw(self.mask, self.offset)
