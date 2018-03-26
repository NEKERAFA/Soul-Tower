# -*- coding: utf-8 -*-

import pygame
from src.sprites.characters.Player import *
from src.sprites.characters.player.PlayerState import *
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
        # Debug:
        # print("Changing state from ", self.name, " to ", state.name)
        self.__class__ = state

    def initializate(self, player):
        speedX = player.speed[0]*self.speedMulti
        speedY = player.speed[1]*self.speedMulti
        self.speed = speedX,speedY

    def calc_final_pos(self, player, mapMask):
        distX = 0
        distY = 0
        width = player.rect.width - 1
        height = player.rect.height - 1
        x, y = player.position
        x = int(x)
        y = int(y - player.rect.height)
        # Calculamos la distancia a avanzar en cada dirección hasta
        # la distancia máxima o hasta colisión
        if (player.movement == N):
            distX = 0
            while (distY<self.maxDist):
                y = int(y - height)
                distY += height
                if (mapMask.overlap_area(player.mask,(x,y))>0):
                    break
            distY = -distY
        elif (player.movement == S):
            distX = 0
            while (distY<self.maxDist):
                y = int(y + height)
                distY += height
                if (mapMask.overlap_area(player.mask,(x,y))>0):
                    break
        elif (player.movement == NW):
            while (distX<self.diagDist):
                x = int(x - width)
                y = int(y - height)
                distX += width
                distY += height
                if (mapMask.overlap_area(player.mask,(x,y))>0):
                    break
            distX = -distX
            distY = -distY
        elif (player.movement == NE):
            while (distX<self.diagDist):
                x = int(x - width)
                y = int(y - height)
                distX += width
                distY += height
                if (mapMask.overlap_area(player.mask,(x,y))>0):
                    break
            distY = -distY
        elif (player.movement == W):
            distY = 0
            while (distX<self.maxDist):
                x = int(x - width)
                distX += width
                if (mapMask.overlap_area(player.mask,(x,y))>0):
                    break
            distX = -distX
        elif (player.movement == E):
            distY = 0
            while (distX<self.maxDist):
                x = int(x + width)
                distX += width
                if (mapMask.overlap_area(player.mask,(x,y))>0):
                    break
        elif (player.movement == SW):
            while (distX<self.diagDist):
                x = int(x - width)
                y = int(y - height)
                distX += width
                distY += height
                if (mapMask.overlap_area(player.mask,(x,y))>0):
                    break
            distX = -distX
        elif (player.movement == SE):
            while (distX<self.diagDist):
                x = int(x - width)
                y = int(y - height)
                distX += width
                distY += height
                if (mapMask.overlap_area(player.mask,(x,y))>0):
                    break

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

    def debug(self):
        print("PlayerState = ", self.name)