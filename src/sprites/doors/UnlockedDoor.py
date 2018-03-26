import pygame
from src.sprites.Door import *

class UnlockedDoor(Door):
    def __init__(self, position, imagePath, stageMask, collision, wait=False):
        Door.__init__(self, position, imagePath, stageMask)
        self.collision = collision
        self.wait = wait

    def open(self, stage):
        if not self.wait or (self.wait): # TODO and stage.mirar_variable):
            stage.mask.erase(self.mask, self.offset)
            self.kill()
