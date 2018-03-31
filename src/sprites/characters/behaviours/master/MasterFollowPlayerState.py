# -*- coding: utf-8 -*-

import random
from src.sprites.characters.behaviours.MasterBehaviourState import *
from src.sprites.characters.behaviours.master.MasterAttack1State import *
from src.sprites.Character import *
from src.sprites.MySprite import *
from src.sprites.EnemyRange import *
from src.sprites.attacks.SemicircleAttack import *

# ------------------------------------------------------------------------------
# Clase MasterFollowPlayerState

class MasterFollowPlayerState(MasterBehaviourState):
    def __init__(self, previousState):
        MasterBehaviourState.__init__(self)
        self.delayTime = random.randint(2, 4)*1000
        self.elapseTime = 0
        self.previousState = previousState
        self.colliding = False

    def move_ai(self, enemy, player):
        self.player = player
        # Obtenemos las posiciones del enemigo y el jugador
        (enemyX, enemyY) = enemy.rect.center
        (playerX, playerY) = player.rect.center

        # Obtenemos el ángulo entre el enemigo y el jugador
        angle = int(math.degrees(math.atan2(enemyY-playerY, playerX-enemyX)))

        # Corrección cuando el ángulo es entre 180-360
        if angle < 0:
            angle = 360 + angle

        # Calculamos hacia donde tiene que moverse el personaje
        lookAt, move = EnemyRange.discretice_angle(angle)

        # Se actualiza el movimiento del personaje
        Character.move(enemy, move)

        # Comprobamos si se está colisionando con el enemigo para volver al
        # otro estado
        if pygame.sprite.collide_rect(player, enemy):
            self.colliding = True
            # enemy.animationLoop = False
            # enemy.animationFinish = False
            # enemy.set_initial_frame(5)
            # enemy.change_behaviour(MasterSlashState(self))
            

    def update(self, enemy, time, mapRect, mapMask):
        # Se actualiza el movimiento del personaje
        Character.update_movement(enemy, time)
        enemy.speed = (enemy.speed[0]*1.5, enemy.speed[1]*1.5)
        MySprite.update(enemy, time)

        self.elapseTime += time
        if self.elapseTime > self.delayTime or self.colliding:
            self.colliding = False
            Character.move(enemy, STILL)
            Character.update_movement(enemy, time)
            enemy.animationLoop = False
            enemy.animationFinish = False
            jump = random.randint(0, 1)
            jump = 1
            if (jump == 0):
                enemy.set_initial_frame(2)
                enemy.attack = SemicircleAttack(pygame.sprite.Group(self.player), enemy.looking)
                enemy.change_behaviour(MasterAttack1State(self))
            # else:
            #     enemy.set_initial_frame(7)
            #     enemy.attack = OrbAttack(1, 500, pygame.sprite.Group(self.player), enemy.looking)
            #     enemy.change_behaviour(MasterCastState(self))

            # Character.update_animation(enemy, time)
            # MySprite.update(enemy, time)
