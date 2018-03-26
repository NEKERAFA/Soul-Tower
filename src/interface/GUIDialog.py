# -*- encoding: utf-8 -*-

import pygame, os
from math import floor, ceil
from src.ResourceManager import *
from src.interface.GUIImage import *

# -------------------------------------------------
# Clase GUIDialog

# Cajas de diálogo
DEFAULT_DIALOG_BOX = 'interface/game/dialog_box.png'
DEFAULT_NAME_BOX = 'interface/game/name_box.png'

# Posición y dimensiones del diálogo
DIALOG_LEFT = 20
DIALOG_BOTTOM = 295
DIALOG_WIDTH = 360
DIALOG_HEIGHT = 100
NAME_LEFT_MARGIN = 11
NAME_TOP_MARGIN = 4

# Posición del texto
TEXT_TOP = DIALOG_BOTTOM - DIALOG_HEIGHT + 23
TEXT_LEFT = DIALOG_LEFT + 20
LINE_SPACE = 20

# Velocidad del texto
DEFAULT_TEXT_SPEED = 0.02

# Escalado de los retratos
PORTRAIT_SCALE = 2

# Fuentes
DEFAULT_FONT = 'PixelOperatorHB.ttf'
DEFAULT_FONT_SIZE = 16
DEFAULT_NAME_SIZE = 14

# TODO poner fuentes en json maybe

class GUIDialog(GUIImage):
    def __init__(self, guiScreen, intervention, dialogBox=DEFAULT_DIALOG_BOX, font=DEFAULT_FONT, fontSize=DEFAULT_FONT_SIZE):
        GUIImage.__init__(self, guiScreen, dialogBox, (DIALOG_LEFT, DIALOG_BOTTOM), None)
        pygame.font.init()

        # Texto a escribir
        self.text = intervention["text"]
        self.index = 0 # Número de bloque de texto
        self.line = 0
        # Fuente del texto
        self.font = ResourceManager.load_font(font, fontSize)
        self.nameFont = ResourceManager.load_font(font, DEFAULT_NAME_SIZE)

        # Variables de control de la impresión
        self.printText = []
        # Inicializamos la lista de líneas a imprimir con tantos strings vacíos como líneas tenga el primer bloque
        for i in range(0, len(self.text[0])):
            self.printText.append("")

        self.textSpeed = DEFAULT_TEXT_SPEED
        self.textCounter = 0

        self.background = pygame.Surface((0,0))

        # Retratos y nombres
        self.rightPortrait = pygame.Surface((0,0))
        self.rightPortraitRect = pygame.Rect((0,0), (0,0))
        self.rightName = None
        self.rightNameRect = pygame.Rect((0,0), (0,0))
        self.leftPortrait = pygame.Surface((0,0))
        self.leftPortraitRect = pygame.Rect((0,0), (0,0))
        self.leftName = None
        self.leftNameRect = pygame.Rect((0,0), (0,0))
        self.nameBox = pygame.Surface((0,0))

        if "info" in intervention:
            self.nameBox = ResourceManager.load_image(DEFAULT_NAME_BOX, -1)
            # Retrato derecho
            if "right" in intervention["info"]:
                self.rightName = intervention["info"]["right"]["name"]
                portraitPath = os.path.join('interface', 'game', intervention["info"]["right"]["image"])
                self.rightPortrait = ResourceManager.load_image(portraitPath, -1)
                # Escalamos la imagen
                self.rightPortraitRect = self.rightPortrait.get_rect()
                self.rightPortrait = pygame.transform.scale(self.rightPortrait, (self.rightPortraitRect.width * PORTRAIT_SCALE, self.rightPortraitRect.height * PORTRAIT_SCALE))
                self.rightPortraitRect = self.rightPortrait.get_rect()
                # La colocamos encima del diálogo, en el borde derecho
                self.rightPortraitRect.right = self.rect.right - 3
                self.rightPortraitRect.bottom = self.rect.top
                # Colocamos la caja de nombre
                self.rightNameRect = self.nameBox.get_rect()
                self.rightNameRect.right = self.rect.right
                self.rightNameRect.bottom = self.rect.top

            # Retrato izquierdo
            if "left" in intervention["info"]:
                self.leftName = intervention["info"]["left"]["name"]
                portraitPath = os.path.join('interface', 'game', intervention["info"]["left"]["image"])
                # Cargamos el retrato dado la vuelta en el eje x
                self.leftPortrait = pygame.transform.flip(ResourceManager.load_image(portraitPath, -1), True, False)
                # Escalamos la imagen
                self.leftPortraitRect = self.leftPortrait.get_rect()
                self.leftPortrait = pygame.transform.scale(self.leftPortrait, (int(self.leftPortraitRect.width * PORTRAIT_SCALE), int(self.leftPortraitRect.height * PORTRAIT_SCALE)))
                self.leftPortraitRect = self.leftPortrait.get_rect()
                # La colocamos encima del diálogo, en el borde izquierdo
                self.leftPortraitRect.left = self.rect.left + 3
                self.leftPortraitRect.bottom = self.rect.top
                # Colocamos la caja de nombre
                self.leftNameRect = self.nameBox.get_rect()
                self.leftNameRect.left = self.rect.left
                self.leftNameRect.bottom = self.rect.top

            # Velocidad de texto
            if "speed" in intervention["info"]:
                self.textSpeed = intervention["info"]["speed"]

            # Imagen de fondo
            if "background" in intervention["info"]:
                backgroundPath = os.path.join('interface', 'backgrounds', intervention["info"]["background"])
                self.background = ResourceManager.load_image(backgroundPath)

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
        # Dibujar la imagen de fondo
        screen.blit(self.background, screen.get_rect())

        # Dibujar la caja del diálogo
        screen.blit(self.image, self.rect)
        # Dibujar el texto
        for i in range(0, len(self.printText)):
            textSurface = self.font.render(self.printText[i], False, (255,255,255))
            screen.blit(textSurface, (TEXT_LEFT, TEXT_TOP + i * LINE_SPACE))
        # Dibujar los retratos
        screen.blit(self.rightPortrait, self.rightPortraitRect)
        screen.blit(self.leftPortrait, self.leftPortraitRect)
        # Dibujar las cajas de nombres
        if self.rightName is not None:
            screen.blit(self.nameBox, self.rightNameRect)
            rightNameText = self.nameFont.render(self.rightName, False, (255,255,255))
            screen.blit(rightNameText, (self.rightNameRect.left + NAME_LEFT_MARGIN, self.rightNameRect.top + NAME_TOP_MARGIN))

        if self.leftName is not None:
            screen.blit(self.nameBox, self.leftNameRect)
            leftNameText = self.nameFont.render(self.leftName, False, (255,255,255))
            screen.blit(leftNameText, (self.leftNameRect.left + NAME_LEFT_MARGIN, self.leftNameRect.top + NAME_TOP_MARGIN))
