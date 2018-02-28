# -*- encoding: utf-8 -*-

# Modulos
import pygame
import sys
#import scene
from Scene import *
from pygame.locals import *


class GameManager():

    def __init__(self):
        # Inicializamos la pantalla y el modo grafico
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Juego con escenas")
        # Pila de escenas
        self.stack = []
        # Flag que nos indica cuando quieren salir de la escena
        self.sceneExit = False
        # Reloj
        self.clock = pygame.time.Clock()


    def loop(self, scene):

        self.sceneExit = False

        # Eliminamos todos los eventos producidos antes de entrar en el loop
        pygame.event.clear()

        # El loop del juego, las acciones que se realicen se harán en cada escena
        while not self.sceneExit:

            # Sincronizar el juego a 60 fps
            elapsedTime = self.clock.tick(60)

            # Pasamos los eventos a la escena
            scene.events(pygame.event.get())

            # Actualiza la escena
            scene.update(elapsedTime)

            # Se dibuja en pantalla
            scene.draw(self.screen)
            pygame.display.flip()


    def run(self):

        # Mientras haya escenas en la pila, ejecutaremos la de arriba
        while (len(self.stack)>0):

            # Se coge la escena a ejecutar como la que este en la cima de la pila
            scene = self.stack[len(self.stack)-1]

            # Ejecutamos el loop de eventos hasta que termine la escena
            self.loop(scene)


    def scene_exit(self):
        # Indicamos en el flag que se quiere salir de la escena
        self.sceneExit = True
        # Eliminamos la escena actual de la pila (si la hay)
        if (len(self.stack)>0):
            self.stack.pop()

    def program_exit(self):
        # Vaciamos la lista de escenas pendientes
        self.stack = []
        self.sceneExit = True

    def scene_change(self, scene):
        self.scene_exit()
        # Ponemos la escena pasada en la cima de la pila
        self.stack.append(scene)

    def scene_stack(self, scene):
        self.sceneExit = True
        # Ponemos la escena pasada en la cima de la pila
        #  (por encima de la actual)
        self.stack.append(scene)
