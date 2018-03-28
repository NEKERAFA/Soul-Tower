# -*- coding: utf-8 -*-

import os
from src.scenes.stage.OnMagicWindowState import *
from src.sprites.MyStaticAnimatedSprite import *
from src.sprites.Interactive import *

SPRITE_PATH = os.path.join('interactives', 'magic_window')

class MagicWindow(MyStaticAnimatedSprite, Interactive):
    def __init__(self, position, initialDialog, selectionFile, endDialogs, collision):
        # Llamamos al constructor de la primera clase
        MyStaticAnimatedSprite.__init__(self, SPRITE_PATH + '.png', SPRITE_PATH + '.json')
        # Cambiamos la posición
        self.change_position(position)
        (posX, posY) = position
        posY = posY - self.rect.height
        self.offset = (posX, posY)
        # Llamamos al constructor de la segunda clase
        collision = pygame.Rect(collision[0], collision[1], collision[2], collision[3])
        Interactive.__init__(self, collision)
        # Guardamos la lista de díalogos y el fichero con la configuración de
        # la selección
        self.initialDialog = initialDialog
        self.selectionFile = selectionFile
        self.endDialogs = endDialogs

    def update(self, time, stage):
        stage.mask.erase(self.mask, self.offset)
        MyStaticAnimatedSprite.update(self, time)
        stage.mask.draw(self.mask, self.offset)

    def destruct(self, stage):
        self.animationLoop = False
        self.animationNum = 1
        self.animationFrame = -1
        self.currentDelay = -1
        self.update(0, stage)

    def activate(self, stage):
        if self.animationLoop:
            stage.state = OnMagicWindowState(self, stage)
