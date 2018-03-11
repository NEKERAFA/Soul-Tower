import pygame
import math as m
from pygame.locals import *
from src.ControlManager import *

class KeyboardMouseControl(ControlManager):
    def __init__(self):
        self.upButton = K_w
        self.downButton = K_s
        self.leftButton = K_a
        self.rightButton = K_d

    def up(self):
        return pygame.key.get_pressed()[self.upButton]
    def down(self):
        return pygame.key.get_pressed()[self.downButton]
    def left(self):
        return pygame.key.get_pressed()[self.leftButton]
    def right(self):
        return pygame.key.get_pressed()[self.rightButton]
    def angle(self, pos):
        (playerX, playerY) = pos
        (mouseX, mouseY) = pygame.mouse.get_pos()
        # Escalado
        mouseX /= 2
        mouseY /= 2
        ang = m.degrees(m.atan2(playerY - mouseY, mouseX - playerX))
        return ang

    def prim_button(self):
        return pygame.mouse.get_pressed()[0]

    def set_key_up(self, newKey):
        self.upButton = newKey
    def set_key_down(self, newKey):
        self.upDown = newKey
    def set_key_left(self, newKey):
        self.upLeft = newKey
    def set_key_right(self, newKey):
        self.upRight = newKey
