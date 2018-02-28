# -*- encoding: utf-8 -*-

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# -------------------------------------------------
# Clase Escena con lo metodos abstractos

class Scene:

    def __init__(self, gameManager):
        self.gameManager = gameManager

    def update(self, *args):
        raise NotImplemented("Tiene que implementar el metodo update.")

    def events(self, *args):
        raise NotImplemented("Tiene que implementar el metodo eventos.")

    def draw(self, screen):
        raise NotImplemented("Tiene que implementar el metodo dibujar.")
