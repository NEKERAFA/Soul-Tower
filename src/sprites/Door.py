# -*- coding: utf-8 -*-

from src.sprites.MyStaticSprite import *
from src.ResourceManager import *
import pygame, os

DOORS_PATH = 'doors'

class Door(MyStaticSprite):
    def __init__(self, position, imagePath, doorMask, stageMask):
        MyStaticSprite.__init__(self)

        self.image = ResourceManager.load_image(os.path.join(DOORS_PATH, imagePath))
        self.rect = self.image.get_rect()
        self.change_position(position)
        self.mask = pygame.mask.Mask(doorMask[2:4])
        self.mask.fill()
        self.offset = doorMask[0:2]
        stageMask.draw(self.mask, self.offset)

    def open(self, stage):
        stage.mask.erase(self.mask, self.offset)
        self.kill()
