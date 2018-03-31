# -*- coding: utf-8 -*-

import pygame, os
from src.sprites.MyStaticSprite import *
from src.sprites.Interactive import *
from src.ResourceManager import *
from src.scenes.stage.OnDialogueState import *

SPRITE_FILES = os.path.join("sprites", "interactives")

class Upgrade(MyStaticSprite, Interactive):
    def __init__(self, position, imageFile, cost, upgrade):
        # Llamamos al constructor de la clase
        MyStaticSprite.__init__(self)
        # Obtenemos la imagen
        self.image = ResourceManager.load_image(os.path.join(SPRITE_FILES, imageFile), -1)
        self.rect = self.image.get_rect()
        self.rect.bottomleft = position
        # Cargamos el objeto interactivo
        Interactive.__init__(self, self.rect)
        # Cambiamos la posición del sprite
        self.change_position(position)
        # Guardamos el coste y de quien es la mejora
        self.cost = cost
        self.upgrade = upgrade

    def activate(self, stage):
        if stage.player.souls >= self.cost:
            # Llamamos al jugador para quitarle almas
            stage.player.decrement_souls(self.cost)
            if self.upgrade == 'ranged':
                # Mejora de leraila
                stage.set_state(OnDialogueState('lerailaUpgrade.json', stage))
                stage.player.rangedLevel += 1
            elif self.upgrade == 'melee':
                # Mejora de Daric
                stage.player.meleeLevel += 1
                stage.set_state(OnDialogueState('daricUpgrade.json', stage))
            # Quitamos el sprite de todos los grupos
            self.kill()
        else:
            dialogue = [{"text": [["Necesitas " + str(self.cost) + " almas para obtener esta"], ["mejora."]]}]
            stage.set_state(OnDialogueState(dialogue, stage, False))
