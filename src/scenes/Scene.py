# -*- encoding: utf-8 -*-

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 300

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 900

# -------------------------------------------------
# Clase Scene con lo metodos abstractos

class Scene(object):
    def __init__(self, gameManager):
        self.gameManager = gameManager

    def update(self, *args):
        raise NotImplemented("Tiene que implementar el metodo update.")

    def events(self, *args):
        raise NotImplemented("Tiene que implementar el metodo eventos.")

    def draw(self, screen):
        raise NotImplemented("Tiene que implementar el metodo dibujar.")
