# -*- encoding: utf-8 -*-

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 300

WINDOW_WIDTH = SCREEN_WIDTH*2
WINDOW_HEIGHT = SCREEN_HEIGHT*2

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
