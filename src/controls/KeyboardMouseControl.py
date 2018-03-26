import pygame
import math as m
from pygame.locals import *
from src.ControlManager import *
from src.scenes.Scene import *

class KeyboardMouseControl(ControlManager):
    upButton = K_w
    downButton = K_s
    leftButton = K_a
    rightButton = K_d
    secButton = K_SPACE
    selectButton = K_e

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
        mouseX /= SCALE_FACTOR
        mouseY /= SCALE_FACTOR
        ang = m.degrees(m.atan2(playerY - mouseY, mouseX - playerX))
        return ang

    @classmethod
    def prim_button(cls):
        return pygame.mouse.get_pressed()[0]

    @classmethod
    def sec_button(cls):
        return pygame.key.get_pressed()[cls.secButton]

    @classmethod
    def select_button(cls):
        return pygame.key.get_pressed()[cls.selectButton]

    @classmethod
    def set_key_up(cls, newKey):
        cls.upButton = newKey

    @classmethod
    def set_key_down(cls, newKey):
        cls.downButton = newKey

    @classmethod
    def set_key_left(cls, newKey):
        cls.leftButton = newKey

    @classmethod
    def set_key_right(cls, newKey):
        cls.rightButton = newKey

    @classmethod
    def set_key_select(cls, newKey):
        cls.selectButton = newKey
