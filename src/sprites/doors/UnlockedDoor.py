import pygame
from src.sprites.Door import *
from src.sprites.Interactive import *

class UnlockedDoor(Door, Interactive):
    def __init__(self, position, imagePath, doorMask, stageMask, collision, attr=None):
        Door.__init__(self, position, imagePath, doorMask, stageMask)
        Interactive.__init__(self, collision)
        self.attr = attr

    def activate(self, stage):
        if self.attr is None or getattr(stage, self.attr):
            stage.mask.erase(self.mask, self.offset)
            self.kill()
