# -*- encoding: utf-8 -*-

import pygame
from math import floor
from src.ResourceManager import *
from src.interface.GUIImage import *

# -------------------------------------------------
# Clase GUIDialog

class GUIDialog(GUIImage):
    def __init__(self, gui_screen, name, position, scale, text):
        GUIImage.__init__(self, gui_screen, name, position, scale)
        pygame.font.init()
        
        self.textPositionX=self.rect.left+20
        self.textPositionY=self.rect.top+50
        self.myfont = pygame.font.SysFont('dejavusans', 14)
        self.fullText = text
        self.printText = ""
        self.textCounter = 0
        self.textSpeed = 0.02
        self.nextLetter = 0

    def update(self, time):

        if(self.textCounter<len(self.fullText)):
            if(self.nextLetter==floor(self.textCounter)):
                self.printText += self.fullText[self.nextLetter]
                self.nextLetter+=1
            self.textCounter+=self.textSpeed*time
        return

    def draw(self, screen):
        textSurface = self.myfont.render(self.printText, False, (0,0,0))
        screen.blit(self.image, self.rect)
        screen.blit(textSurface, (self.textPositionX, self.textPositionY))

    def action(self):
        #No hace nada (es una imagen)
        return
