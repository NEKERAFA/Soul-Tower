# -*- coding: utf-8 -*-

class State(object):

    def __init__(self):
        pass

    def update(self, time):
        raise NotImplemented("Tiene que implementar el metodo update.")

    def draw(self, screen):
        raise NotImplemented("Tiene que implementar el metodo draw.")

    def events(self, events):
        raise NotImplemented("Tiene que implementar el metodo events.")
