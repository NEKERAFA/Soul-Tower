import pygame
import math as m
from pygame.locals import *
from src.ControlManager import *

# TODO actualizar en UML
class KeyboardMouseControl(ControlManager):
    upButton = K_w
    downButton = K_s
    leftButton = K_a
    rightButton = K_d
    secButton = K_SPACE

    @classmethod
    def up(cls):
        return pygame.key.get_pressed()[cls.upButton]

    @classmethod
    def down(cls):
        return pygame.key.get_pressed()[cls.downButton]

    @classmethod
    def left(cls):
        return pygame.key.get_pressed()[cls.leftButton]

    @classmethod
    def right(cls):
        return pygame.key.get_pressed()[cls.rightButton]

    @classmethod
    def angle(cls, pos):
        (playerX, playerY) = pos
        (mouseX, mouseY) = pygame.mouse.get_pos()
        # Escalado
        mouseX /= 2
        mouseY /= 2
        ang = m.degrees(m.atan2(playerY - mouseY, mouseX - playerX))
        return ang

    @classmethod
    def prim_button(cls):
        return pygame.mouse.get_pressed()[0]

    @classmethod
    def sec_button(cls):
        return pygame.key.get_pressed()[cls.secButton]

    @classmethod
    def set_key_up(cls, newKey):
        cls.upButton = newKey

    @classmethod
    def set_key_down(cls, newKey):
        cls.upDown = newKey

    @classmethod
    def set_key_left(cls, newKey):
        cls.upLeft = newKey

    @classmethod
    def set_key_right(cls, newKey):
        cls.upRight = newKey
