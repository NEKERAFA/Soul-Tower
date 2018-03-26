# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
# Clase padre para controlar el cambio de estado

class ChangingState(object):
    def update(self, player, time, stage):
        raise NotImplemented("Tiene que implementar el metodo update")
