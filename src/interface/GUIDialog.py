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
LINE_SPACE = 20 # TODO ajustar

# Escalado de los retratos
PORTRAIT_SCALE = 2

# TODO constante con el path de la imagen del diálogo?


class GUIDialog(GUIImage):
    def __init__(self, gui_screen, name, position, scale, font, intervention, textSpeed=0.02):
        GUIImage.__init__(self, gui_screen, name, position, scale)
        pygame.font.init()

        # Texto a escribir
        self.text = intervention["text"]
        self.index = 0 # Número de bloque de texto
        self.line = 0
        # Fuente del texto
        self.font = font

        # Variables de control de la impresión
        self.printText = []
        # Inicializamos la lista de líneas a imprimir con tantos strings vacíos como líneas tenga el primer bloque
        for i in range(0, len(self.text[0])):
            self.printText.append("")

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

            # Retrato izquierdo
            if "left" in intervention["info"]:
                self.leftName = intervention["info"]["left"]["name"]
                portraitPath = os.path.join('interface', 'game', intervention["info"]["left"]["image"])
                # Cargamos el retrato dado la vuelta en el eje x
                self.leftPortrait = pygame.transform.flip(ResourceManager.load_image(portraitPath, -1), True, False)
                # Escalamos la imagen
                self.leftPortraitRect = self.leftPortrait.get_rect()
                self.leftPortrait = pygame.transform.scale(self.leftPortrait, (self.leftPortraitRect.width * PORTRAIT_SCALE, self.leftPortraitRect.height * PORTRAIT_SCALE))
                self.leftPortraitRect = self.leftPortrait.get_rect()
                # Lo colocamos encima del diálogo, en el borde izquierdo
                self.leftPortraitRect.left = self.rect.left
                self.leftPortraitRect.bottom = self.rect.top

    # Pasa al siguiente bloque de texto, reseteando contadores y variables
    def next(self):
        self.index += 1
        if self.index < len(self.text):
            self.line = 0
            self.textCounter = 0
            self.printText = []
            for i in range(0, len(self.text[self.index])):
                self.printText.append("")

    # Devuelve True en caso de que ya no queden bloques de texto por mostrar; False en caso contrario
    def is_finished(self):
        return (self.index == len(self.text)-1)

    def update(self, time):
        # Si quedan bloques por imprimir
        if self.index < len(self.text):
            block = self.text[self.index]
            # Si quedan líneas por imprimir
            if (self.line < len(self.text[self.index])):
                maxSize = len(block[self.line])
                lineText = block[self.line]
                # Si queda texto por imprimir en la línea, calculamos cuántas letras debemos mostrar (en base al tiempo y la velocidad)
                # las mostramos e incrementamos el contador
                if (self.textCounter < maxSize):
                    letters = int(ceil(self.textSpeed * time)) # Redondeamos hacia arriba para garantizar al menos una letra por frame
                    limit = min(maxSize, self.textCounter + letters) # Nos aseguramos de no pasarnos de los límites del index
                    self.printText[self.line] += lineText[self.textCounter:(self.textCounter + letters)] # Añadimos las próximas letras a escribir
                    self.textCounter += letters
                    # Si hemos llegado al final de la línea, pasamos a la siguiente
                    if (self.textCounter >= maxSize):
                        self.textCounter = 0
                        self.line += 1

    def draw(self, screen):
        # Dibujar la imagen de fondo del diálogo (la caja)
        screen.blit(self.image, self.rect)
        # Dibujar el texto
        for i in range(0, len(self.printText)):
            textSurface = self.font.render(self.printText[i], False, (0,0,0))
            screen.blit(textSurface, (TEXT_LEFT, TEXT_TOP + i * LINE_SPACE))
        # Dibujar los retratos
        screen.blit(self.rightPortrait, self.rightPortraitRect)
        screen.blit(self.leftPortrait, self.leftPortraitRect)
