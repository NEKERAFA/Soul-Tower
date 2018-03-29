# -*- coding: utf-8 -*-

import pygame, os
from src.ResourceManager import *
from src.sprites.Collectable import *
from src.sprites.MyStaticAnimatedSprite import *

DROP_PATH = 'drops'

# -------------------------------------------------
# Clase Drop

class Drop(MyStaticAnimatedSprite,  Collectable):
    def __init__(self, spriteName, amount):
        # Nombre del drop
        self.name = spriteName

        # Obtenemos el nombre de la carpeta del sprite sheet y del archivo de configuración
        fullname = os.path.join(DROP_PATH, spriteName)
        # Primero invocamos al constructor de la clase padre
        MyStaticAnimatedSprite.__init__(self, fullname + '.png', fullname + '.json')
        # Cantidad de elementos del Drop
        self.amount = amount

    def collect(self, stage):
        # Drops de vida
        if self.name == 'heart':
            # Comprobamos que la vida del enemigo es menor que la máxima
            # (ha recibido daño)
            if stage.player.stats["hp"] < stage.player.stats["max_hp"]:
                # Añadimos las vidas al jugador
                stage.player.add_lifes(self.amount)
                # Eliminamos el sprite de todos los grupos
                self.kill()
        # Drops de almas
        elif self.name == 'soul':
            # Añadimos las almas recogidas y eliminamos el sprite de todos
            # los grupos
            stage.player.increase_souls(self.amount)
            self.kill()
