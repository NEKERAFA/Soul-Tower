# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
# Clase BehaviourState

class BehaviourState(object):
    def move_ai(player):
        raise NotImplemented("Tiene que implementar el metodo move_ai.")

    def switch(self, state):
        self.__class__ = state
