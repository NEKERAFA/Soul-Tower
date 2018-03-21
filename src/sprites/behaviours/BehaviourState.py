# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
# Clase BehaviourState

class BehaviourState(object):
    def move_ai(self, enemy, player):
        raise NotImplemented("Tiene que implementar el metodo move_ai.")

    def update(self, enemy, time, mapRect, mapMask):
        raise NotImplemented("Tiene que implementar el metodo update")
