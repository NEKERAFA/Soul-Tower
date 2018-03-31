# -*- coding: utf-8 -*-

import random
from src.sprites.characters.behaviours.RavenBehaviourState import *
from src.sprites.Character import *
from src.sprites.MySprite import *
from src.sprites.EnemyRange import *

# ------------------------------------------------------------------------------
# Clase RavenLandState

class RavenLandState(RavenBehaviourState):
    def __init__(self, position, previousState):
        print "Raven: Land", position
        RavenBehaviourState.__init__(self)
        self.position = position
        self.distance = 0
        self.elapseTime = 0
        self.delayTime = random.randint(2, 5)*1000
        self.land = False
        self.previousState = previousState

    def move_ai(self, enemy, player):
        if not self.land:
            # Obtenemos las posiciones del enemigo y el jugador
            (enemyX, enemyY) = enemy.rect.center
            (x, y) = self.position

            # Actualizamos la distancia al jugador
            self.distance = math.hypot(x-enemyX, y-enemyY)

            # Obtenemos el ángulo entre el enemigo y el jugador
            angle = int(math.degrees(math.atan2(enemyY-y, x-enemyX)))

            # Corrección cuando el ángulo es entre 180-360
            if angle < 0:
                angle = 360 + angle

            # Calculamos hacia donde tiene que moverse el personaje
            lookAt, move = EnemyRange.discretice_angle(angle)

            # Se actualiza el movimiento del personaje
            Character.move(enemy, move)
        else:
            Character.move(enemy, STILL)

    def update(self, enemy, time, mapRect, mapMask):
        # Se actualiza el movimiento del personaje
        Character.update_movement(enemy, time)
        MySprite.update(enemy, time)

        if self.land:
            # Si el cuervo ha aterrizado
            self.elapseTime += time
            # Si ha pasado ya los segundos posado
            if self.elapseTime > self.delayTime:
                enemy.change_behaviour(self.previousState)
        elif self.distance < enemy.rect.width/2:
            # El cuervo sigue volando pero está en la zona de posarse
            self.land = True

    def receive_damage(self, enemy, attack, damage, force):
        if self.land or attack == 'magic':
            Character.receive_damage(enemy, damage, force)
