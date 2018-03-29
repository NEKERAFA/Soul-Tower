# -*- coding: utf-8 -*-

import random
from src.sprites.characters.behaviours.RavenBehaviourState import *
from src.sprites.characters.behaviours.raven.RavenFollowPlayerState import *
from src.sprites.characters.behaviours.raven.RavenLandState import *
from src.sprites.Character import *
from src.sprites.MySprite import *
from src.sprites.EnemyRange import *

# ------------------------------------------------------------------------------
# Clase RavenFlyAroundStageState

class RavenFlyAroundStageState(RavenBehaviourState):
    def __init__(self):
        RavenBehaviourState.__init__(self)
        self.delayTime = random.randint(2, 5)*1000
        self.elapseTime = 0
        self.angle = random.randint(0, 360)

    def move_ai(self, enemy, player):
        pass

    def update(self, enemy, time, mapRect, mapMask):
        # Miramos si el enemigo se sale del area de vuelo
        if not mapRect.inflate(-96, -96).contains(enemy.rect):
            self.angle = random.randint(0, 359)

        # Calculamos hacia donde tiene que moverse el personaje
        lookAt, move = EnemyRange.discretice_angle(self.angle)

        # Se actualiza el movimiento del personaje
        Character.move(enemy, move)
        Character.update_movement(enemy, time)
        MySprite.update(enemy, time)

        # Actualizamos el tiempo interno
        self.elapseTime += time

        # Si se pasan los segundos volando, cambio de estado
        if self.elapseTime > self.delayTime:
            self.delayTime = random.randint(2, 5)*1000
            self.elapseTime = 0
            # Miramos a que estado saltar
            jump = random.randint(0, 1)
            if jump == 1:
                # Cambio de estado
                enemy.change_behaviour(RavenFollowPlayerState(self))
            else:
                # Posiciones del mapa
                x, y = mapRect.topleft
                width, height = mapRect.size
                # Posicion random para posarse
                posX = random.randint(x+48, x+width-48)
                posY = random.randint(y+48, y+height-48)
                # Cambio de estado
                enemy.change_behaviour(RavenLandState((posX, posY), self))

    def receive_damage(self, enemy, attack, damage, force):
        if attack == 'magic':
            Character.receive_damage(enemy, damage, force)
