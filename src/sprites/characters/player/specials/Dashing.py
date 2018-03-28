# -*- coding: utf-8 -*-

import pygame
from src.sprites.characters.Player import *
from src.sprites.characters.player.specials.PlayerState import *
from src.sprites.MySprite import *
import math as m

class Dashing(PlayerState):
    name = "dashing"
    maxDist = 100 # Distancia máxima de dash
    diagDist = m.sqrt((maxDist * maxDist)/2.0)
    dist = maxDist
    travelled = (0,0)
    speedMulti = 8 # multiplicador de velocidad (píxeles / ms)
    dashing = False

    def change(self, player, state):
        # No cambia de estado hasta que termine el dash
        if not self.dashing:
            self.__class__ = state
            # Debug:
            # print("Changing state from ", self.name, " to ", state.name)

    def initializate(self, player):
        speedX = player.speed[0]*self.speedMulti
        speedY = player.speed[1]*self.speedMulti
        self.speed = speedX,speedY

    # Función auxiliar para calcular la distancia que se debe avanzar
    # p1 y p2 son parámetros para controlar la dirección
    def aux_loop(self, playerMask, mapMask, maxDist, x, y, p1, p2):
        distX = 0
        distY = 0
        dist = 0
        x = int(x + 1*p1)
        y = int(y + 1*p2)
        while (dist<maxDist):
            x = int(x + 1*p1)
            y = int(y + 1*p2)
            distX += 1
            distY += 1
            dist += 1
            if (mapMask.overlap_area(playerMask,(x,y))>0):
                distX -= 1
                distY -= 1
                break
        distX = distX * p1
        distY = distY * p2
        return distX,distY

    # Calcula la posición en la que debe acabar el personaje
    def calc_final_pos(self, player, mapMask):
        distX = 0
        distY = 0
        x, y = player.position
        x = int(x)
        y = int(y - player.rect.height)
        # Calculamos la distancia a avanzar en cada dirección hasta
        # la distancia máxima o hasta colisión
        if (player.movement == N):
            distX, distY = self.aux_loop(player.mask, mapMask, self.maxDist, x, y, 0, -1)
        elif (player.movement == S):
            distX, distY = self.aux_loop(player.mask, mapMask, self.maxDist, x, y, 0, 1)
        elif (player.movement == NW):
            distX, distY = self.aux_loop(player.mask, mapMask, self.diagDist, x, y, -1, -1)
        elif (player.movement == NE):
            distX, distY = self.aux_loop(player.mask, mapMask, self.diagDist, x, y, 1, -1)
        elif (player.movement == W):
            distX, distY = self.aux_loop(player.mask, mapMask, self.maxDist, x, y, -1, 0)
        elif (player.movement == E):
            distX, distY = self.aux_loop(player.mask, mapMask, self.maxDist, x, y, 1, 0)
        elif (player.movement == SW):
            distX, distY = self.aux_loop(player.mask, mapMask, self.diagDist, x, y, -1, 1)
        elif (player.movement == SE):
            distX, distY = self.aux_loop(player.mask, mapMask, self.diagDist, x, y, 1, 1)
        self.dist = distX,distY

    def update_state(self, player, time, mapRect, mapMask):
        # Si estamos empezando a dashear, inicializamos todo
        if not self.dashing:
            Character.update_movement(player, time)
            self.dashing = True
            self.initializate(player)
            self.calc_final_pos(player, mapMask)
        # Si hemos llegado al destino
        if (abs(self.travelled[0])>=abs(self.dist[0]) and abs(self.travelled[1])>=abs(self.dist[1])):
            # reiniciamos valores
            self.travelled = (0,0)
            # y volvemos al estado normal
            self.dashing = False
            self.change(player, Normal)
            self.lastDash = 0

        else: # Si aun no hemos llegado
            # actualizamos el tiempo que llevamos de dash
            # y calculamos la debida posición respecto a ello
            incrementX = self.speed[0]*time
            incrementY = self.speed[1]*time
            self.travelled = self.travelled[0]+incrementX, self.travelled[1]+incrementY
            MySprite.increment_position(player, (incrementX,incrementY))

        # Comprobación de colisiones
        x, y = player.position
        x = int(x)
        y = int(y - player.rect.height)
        distX,distY = self.dist
        # Se desplaza el personaje en la dirección adecuada
        # hasta que deje de colisionar
        if (distX!=0 or distY!=0):
            while(mapMask.overlap_area(player.mask,(x,y))>0):
                x,y = player.position
                x = int(x)
                y = int(y - player.rect.height)
                if (distX>0):
                    incrX = -1
                elif (distX<0):
                    incrX = 1
                else:
                    incrX = 0
                if (distY>0):
                    incrY = -1
                elif (distY<0):
                    incrY = 1
                else:
                    incrY = 0
                MySprite.increment_position(player, (incrX,incrY))
        else:
            # Se calculan los "gradientes" para conocer la dirección de la colisión
            dx = mapMask.overlap_area(player.mask,(x+1,y)) - mapMask.overlap_area(player.mask,(x-1,y))
            dy = mapMask.overlap_area(player.mask,(x,y+1)) - mapMask.overlap_area(player.mask,(x,y-1))
            while(dx or dy):
                if (dx>0):
                    incrX = -1
                elif (dx<0):
                    incrX = 1
                else:
                    incrX = 0
                if (dy>0):
                    incrY = -1
                elif (dy<0):
                    incrY = 1
                else:
                    incrY = 0
                MySprite.increment_position(player, (incrX, incrY))
                x, y = player.rect.topleft
                dx = mapMask.overlap_area(player.mask, (x+1,y)) - mapMask.overlap_area(player.mask, (x-1,y))
                dy = mapMask.overlap_area(player.mask, (x,y+1)) - mapMask.overlap_area(player.mask, (x,y-1))

    def receive_damage_aux(self, player, force):
        # Invulnerable
        return

    def debug(self):
        print("PlayerState = ", self.name)
