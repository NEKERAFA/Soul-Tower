# -*- coding: utf-8 -*-

from src.sprites.Drop import *
from src.sprites.Ring import *


class DropConstructor(object):
    @classmethod
    def get_drop(cls, dropInfo):
        if dropInfo['type'] == 'ring':
            return Ring(dropInfo['type'], dropInfo['dialogueList'])
        else:
            return Drop(dropInfo['type'], dropInfo['amount'])
