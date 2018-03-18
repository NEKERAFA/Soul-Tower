# -*- coding: utf-8 -*-

class StageState(object):

    def __init__(self):
        pass

    def update(self, time, stage):
        raise NotImplemented("Tiene que implementar el metodo update.")

    def draw(self, screen, stage):
        raise NotImplemented("Tiene que implementar el metodo draw.")

    def events(self, events, stage):
        raise NotImplemented("Tiene que implementar el metodo events.")
