# -*- encoding: utf-8 -*-

import pygame, os
from math import floor, ceil
from src.ResourceManager import *
from src.interface.GUIImage import *

# -------------------------------------------------
# Clase GUIDialog
# TODO poner constantes que indiquen donde se pone una imagen a la izquierda y donde una a la derecha
# (en principio no las necesito si las pongo pegadas al diálogo)

# Posición y dimensiones del diálogo
DIALOG_LEFT = 20
DIALOG_BOTTOM = 295
DIALOG_WIDTH = 360
DIALOG_HEIGHT = 100

# Posición del texto
TEXT_TOP = DIALOG_BOTTOM - DIALOG_HEIGHT + 35
TEXT_LEFT = DIALOG_LEFT + 20
LINE_SPACE = 35 # TODO ajustar

# Escalado de los retratos
PORTRAIT_SCALE = 2

# TODO constante con el path de la imagen del diálogo?


class GUIDialog(GUIImage):
    def __init__(self, gui_screen, name, position, scale, font, intervention, textSpeed=0.02):
        GUIImage.__init__(self, gui_screen, name, position, scale)
        pygame.font.init()

        # Texto a escribir
        self.text = intervention["text"]
        self.index = 0 # TODO usar para avanzar el diálogo
        self.maxSize = len(self.text) # TODO cambiar para que funcione con la lista de líneas
        # Fuente del texto
        self.font = font

        # Variables de control de la impresión
        self.printText = ""
        self.textCounter = 0
        self.textSpeed = textSpeed

        # Retratos y nombres
        # TODO nombres necesitan otro recuadrito de diálogo
        self.rightPortrait = pygame.Surface((0,0))
        self.rightPortraitRect = pygame.Rect((0,0), (0,0))
        self.rightName = None
        self.leftPortrait = pygame.Surface((0,0))
        self.leftPortraitRect = pygame.Rect((0,0), (0,0))
        self.leftName = None

        if "info" in intervention:
            # Retrato derecho
            if "right" in intervention["info"]:
                self.rightName = intervention["info"]["right"]["name"]
                portraitPath = os.path.join('interface', 'game', intervention["info"]["right"]["image"])
                self.rightPortrait = ResourceManager.load_image(portraitPath, -1)
                # Escalamos la imagen
                self.rightPortraitRect = self.rightPortrait.get_rect()
                self.rightPortrait = pygame.transform.scale(self.rightPortrait, (self.rightPortraitRect.width * PORTRAIT_SCALE, self.rightPortraitRect.height * PORTRAIT_SCALE))
                self.rightPortraitRect = self.rightPortrait.get_rect()
                # Lo colocamos encima del diálogo, en el borde derecho
                self.rightPortraitRect.right = self.rect.right
                self.rightPortraitRect.bottom = self.rect.top

            # Retrato izquierdo TODO flipear
            if "left" in intervention["info"]:
                self.leftName = intervention["info"]["left"]["name"]
                portraitPath = os.path.join('interface', 'game', intervention["info"]["left"]["image"])
                self.leftPortrait = ResourceManager.load_image(portraitPath, -1)
                self.leftPortraitRect = self.leftPortrait.get_rect()
                # Lo colocamos encima del diálogo, en el borde izquierdo
                self.leftPortraitRect.left = self.rect.left
                self.leftPortraitRect.bottom = self.rect.top


        # path = os.path.join('interface', 'game', 'leraila.png')
        # self.portrait = ResourceManager.load_image(path, -1)
        # self.portrait_rect = self.portrait.get_rect()
        # self.portrait_pos = (self.rect.right -self.portrait_rect.width-5, self.rect.bottom -5)
        # self.portrait_rect.left = self.portrait_pos[0]
        # self.portrait_rect.bottom = self.portrait_pos[1]

    def update(self, time):
        # Si queda texto por imprimir, calculamos cuántas letras debemos mostrar (en base al tiempo y la velocidad)
        # las mostramos e incrementamos el contador
        if (self.textCounter < self.maxSize):
            letters = int(ceil(self.textSpeed * time)) # Redondeamos hacia arriba para garantizar al menos una letra por frame
            limit = min(self.maxSize, self.textCounter + letters) # Nos aseguramos de no pasarnos de los límites del index
            self.printText += self.text[self.textCounter:(self.textCounter + letters)] # Añadimos las próximas letras a escribir
            self.textCounter += letters


    def draw(self, screen):
        # Crear surface con el texto
        textSurface = self.font.render(self.printText, False, (0,0,0))
        # Dibujar la imagen de fondo del diálogo (la caja)
        screen.blit(self.image, self.rect)
        # Dibujar el texto
        screen.blit(textSurface, (TEXT_LEFT, TEXT_TOP))
        # Dibujar los retratos
        screen.blit(self.rightPortrait, self.rightPortraitRect)
        screen.blit(self.leftPortrait, self.leftPortraitRect)
