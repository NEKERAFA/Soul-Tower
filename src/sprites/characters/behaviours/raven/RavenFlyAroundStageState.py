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
        # Miramos si el enemigo se sale del área de vuelo
        if not mapRect.inflate(-48, -48).contains(enemy.rect):
            if enemy.rect.top < mapRect.top+24:
                # Choca arriba
                if enemy.rect.left < mapRect.left+24:
                    # Choca arriba a la izquierda
                    self.angle = 315
                elif enemy.rect.right > mapRect.right-24:
                    # Choca arriba a la derecha
                    self.angle = 225
                else:
                    self.angle = random.randint(225, 315)
            elif enemy.rect.bottom > mapRect.bottom-24:
                # Choca abajo
                if enemy.rect.left < mapRect.left+24:
                    # Choca abajo a la izquierda
                    self.angle = 45
                elif enemy.rect.right > mapRect.right-24:
                    # Choca abajo a la derecha
                    self.angle = 135
                else:
                    self.angle = random.randint(45, 135)
            # Choca a la izquierda
            elif enemy.rect.left < mapRect.left+24:
                self.angle = random.randint(315, 405) % 360
            # Choca a la derecha
            elif enemy.rect.right > mapRect.right-24:
                self.angle = random.randint(135, 225)
            else:
                print "No se que hacer"
                self.angle = random.randint(0, 356)

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
                posX = random.randint(x+24, x+width-24)
                posY = random.randint(y+24, y+height-24)
                # Cambio de estado
                enemy.change_behaviour(RavenLandState((posX, posY), self))

    def receive_damage(self, enemy, attack, damage, force):
        if attack == 'magic':
            Character.receive_damage(enemy, damage, force)
