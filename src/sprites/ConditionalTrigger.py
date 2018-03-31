# -*- coding: utf-8 -*-

import pygame, os
from src.sprites.Trigger import *

class ConditionalTrigger(Trigger):
    def __init__(self, rect, dialogueList):
        Trigger.__init__(self, rect, dialogueList, None)

    def activate(self, player):
        raise "Must implement activate"
