import pygame, sys, os
import math as m

from pygame.locals import *
from src.ResourceManager import *

class Channel_Effect():

    def __init__(self, sound_effect, reserved_channel, delay):
        #Sonido que se va a reproducir
        self.sound_effect = sound_effect
        #self.sound_effect = ResourceManager.load_effect_sound('pew.wav')

        #Canal reservado
        self.reserved_channel = reserved_channel

        #Delay
        self.delay = delay

        #Current delay
        self.current_delay = 0

    def soundUpdate(self, time):
        self.current_delay -= time
        #print(self.current_delay)
        if self.current_delay < 0:
            self.reserved_channel.play(self.sound_effect)
            self.current_delay = self.delay
