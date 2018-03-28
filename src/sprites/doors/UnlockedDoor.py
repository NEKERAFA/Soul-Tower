import pygame
from src.sprites.Door import *
from src.sprites.Interactive import *

class UnlockedDoor(Door, Interactive):
    def __init__(self, position, imagePath, stageMask, collision, wait):
        Door.__init__(self, position, imagePath, stageMask)
        Interactive.__init__(self, collision)
        self.wait = wait

    def activate(self, stage):
        if not self.wait or (self.wait): # TODO and stage.mirar_variable):
            stage.mask.erase(self.mask, self.offset)
            self.kill()
