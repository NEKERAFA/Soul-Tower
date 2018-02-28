# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
from src.scenes.Scene import *
from src.scenes.Background import *
from src.screens.Room import *

# -------------------------------------------------
# -------------------------------------------------
# Constantes
# -------------------------------------------------
# -------------------------------------------------

# Los bordes de la pantalla para hacer scroll horizontal
#MINIMO_X_JUGADOR = 0
#MAXIMO_X_JUGADOR = ANCHO_PANTALLA - MINIMO_X_JUGADOR

# -------------------------------------------------
# Clase Stage

class InitialStage(Scene):
	def __init__(self, gameManager):

		# Habria que pasarle como parámetro el número de fase, a partir del cual se cargue
		#  un fichero donde este la configuracion de esa fase en concreto, con cosas como
		#   - Nombre del archivo con el decorado
		#   - Posiciones de las plataformas
		#   - Posiciones de los enemigos
		#   - Posiciones de inicio de los jugadores
		#  etc.
		# Y cargar esa configuracion del archivo en lugar de ponerla a mano, como aqui abajo
		# De esta forma, se podrian tener muchas fases distintas con esta clase

		# Primero invocamos al constructor de la clase padre
		Scene.__init__(self, gameManager)

		# Creamos el decorado y el fondo
		#self.decorado = Decorado()
		self.background = Background()
		self.rooms = [Room('initialstage/floor_1.tmx', 'initialstage/floor_1.json')]
		self.current_room = 0

		# Que parte del decorado estamos visualizando
		self.scroll = (0, 0)
		#  En ese caso solo hay scroll horizontal
		#  Si ademas lo hubiese vertical, seria self.scroll = (0, 0)

		# Creamos los sprites de los jugadores
		#self.jugador1 = Jugador()
		#self.jugador2 = Jugador()
		#self.grupoJugadores = pygame.sprite.Group( self.jugador1, self.jugador2 )

		# Ponemos a los jugadores en sus posiciones iniciales
		# self.jugador1.establecerPosicion((200, 551))
		# self.jugador2.establecerPosicion((400, 551))

		# Creamos las plataformas del decorado
		# La plataforma que conforma todo el suelo
		# plataformaSuelo = Plataforma(pygame.Rect(0, 550, 1200, 15))
		# # La plataforma del techo del edificio
		# plataformaCasa = Plataforma(pygame.Rect(870, 417, 200, 10))
		# # y el grupo con las mismas
		# self.grupoPlataformas = pygame.sprite.Group( plataformaSuelo, plataformaCasa )
		#
		# # Y los enemigos que tendran en este decorado
		# enemigo1 = Sniper()
		# enemigo1.establecerPosicion((1000, 418))
		#
		# # Creamos un grupo con los enemigos
		# self.grupoEnemigos = pygame.sprite.Group( enemigo1 )
		#
		# # Creamos un grupo con los Sprites que se mueven
		# #  En este caso, solo los personajes, pero podría haber más (proyectiles, etc.)
		# self.grupoSpritesDinamicos = pygame.sprite.Group( self.jugador1, self.jugador2, enemigo1 )
		# # Creamos otro grupo con todos los Sprites
		# self.grupoSprites = pygame.sprite.Group( self.jugador1, self.jugador2, enemigo1, plataformaSuelo, plataformaCasa )
		#
		# # Creamos las animaciones de fuego,
		# #  las que estan detras del decorado, y delante
		#
		# self.animacionesDetras = []
		# '''for i in range(9):
		# 	# La animacion del fuego
		# 	animacionFuego = AnimacionFuego()
		# 	# Aumentamos un poco el tamaño de la animacion
		# 	animacionFuego.scale((400,400))
		# 	# La situamos en su posicion
		# 	animacionFuego.posicionx = 120*i - 200
		# 	animacionFuego.posiciony = 250
		# 	# Iniciamos la animacion
		# 	animacionFuego.play()
		# 	animacionFuego.nextFrame(i)
		# 	# y la anadimos a la lista de animaciones detras
		# 	self.animacionesDetras.append(animacionFuego)
		# '''
		#
		# animacionFuego = AnimacionFuego()
		# animacionFuego.scale((400,400))
		# animacionFuego.posicionx = 100
		# animacionFuego.posiciony = 100
		# animacionFuego.getRect().bottomright = (0,0)
		#
		# animacionFuego.play()
		#
		# self.animacionesDetras.append(animacionFuego)
		#
		# self.animacionesDelante = []
		# for i in range(11):
		# 	# La animacion del fuego
		# 	animacionFuego = AnimacionFuego()
		# 	# Aumentamos un poco el tamaño de la animacion
		# 	animacionFuego.scale((450,450))
		# 	# La situamos en su posicion
		# 	animacionFuego.posicionx = 120*i - 200
		# 	animacionFuego.posiciony = 450
		# 	# Iniciamos la animacion
		# 	animacionFuego.play()
		# 	animacionFuego.nextFrame(i)
		# 	# y la anadimos a la lista de animaciones delante
		# 	self.animacionesDelante.append(animacionFuego)

	# def actualizarScroll(self, jugador1, jugador2):
	# 	# Se ordenan los jugadores según el eje x, y se mira si hay que actualizar el scroll
	# 	if (jugador1.posicion[0]<jugador2.posicion[0]):
	# 		cambioScroll = self.actualizarScrollOrdenados(jugador1, jugador2)
	# 	else:
	# 		cambioScroll = self.actualizarScrollOrdenados(jugador2, jugador1)
	#
	# 	# Si se cambio el scroll, se desplazan todos los Sprites y el decorado
	# 	if cambioScroll:
	# 		# Actualizamos la posición en pantalla de todos los Sprites según el scroll actual
	# 		for sprite in iter(self.grupoSprites):
	# 			sprite.establecerPosicionPantalla((self.scrollx, 0))
	#
	# 		# Ademas, actualizamos el decorado para que se muestre una parte distinta
	# 		self.decorado.update(self.scrollx)



	# Se actualiza el decorado, realizando las siguientes acciones:
	#  Se indica para los personajes no jugadores qué movimiento desean realizar según su IA
	#  Se mueven los sprites dinámicos, todos a la vez
	#  Se comprueba si hay colision entre algun jugador y algun enemigo
	#  Se comprueba si algún jugador ha salido de la pantalla, y se actualiza el scroll en consecuencia
	#     Actualizar el scroll implica tener que desplazar todos los sprites por pantalla
	#  Se actualiza la posicion del sol y el color del cielo
	def update(self, time):

		# Primero, se indican las acciones que van a hacer los enemigos segun como esten los jugadores
		# for enemigo in iter(self.grupoEnemigos):
		# 	enemigo.mover_cpu(self.jugador1, self.jugador2)
		# # Esta operación es aplicable también a cualquier Sprite que tenga algún tipo de IA
		# # En el caso de los jugadores, esto ya se ha realizado
		#
		# # Actualizamos los Sprites dinamicos
		# # De esta forma, se simula que cambian todos a la vez
		# # Esta operación de update ya comprueba que los movimientos sean correctos
		# #  y, si lo son, realiza el movimiento de los Sprites
		# self.grupoSpritesDinamicos.update(self.grupoPlataformas, time)
		# # Dentro del update ya se comprueba que todos los movimientos son válidos
		# #  (que no choque con paredes, etc.)
		#
		# # Los Sprites que no se mueven no hace falta actualizarlos,
		# #  si se actualiza el scroll, sus posiciones en pantalla se actualizan más abajo
		# # En cambio, sí haría falta actualizar los Sprites que no se mueven pero que tienen que
		# #  mostrar alguna animación
		#
		# # Comprobamos si hay colision entre algun jugador y algun enemigo
		# # Se comprueba la colision entre ambos grupos
		# # Si la hay, indicamos que se ha finalizado la fase
		# if pygame.sprite.groupcollide(self.grupoJugadores, self.grupoEnemigos, False, False)!={}:
		# 	# Se le dice al director que salga de esta escena y ejecute la siguiente en la pila
		# 	self.director.salirEscena()
		#
		# # Actualizamos el scroll
		# self.actualizarScroll(self.jugador1, self.jugador2)
		# # Actualizamos el fondo:
		#  la posicion del sol y el color del cielo
		self.background.update(time)


	def draw(self, screen):
		# Ponemos primero el fondo
		self.background.draw(screen)
		# Despues, las animaciones que haya detras
		# for animacion in self.animacionesDetras:
		# 	animacion.dibujar(pantalla)
		# # Después el decorado
		# self.decorado.dibujar(pantalla)
		# # Luego los Sprites
		# self.grupoSprites.draw(pantalla)
		# # Y por ultimo, dibujamos las animaciones por encima del decorado
		# for animacion in self.animacionesDelante:
		# 	animacion.dibujar(pantalla)
		self.rooms[self.current_room].draw(screen)


	def events(self, event_list):
		# Miramos a ver si hay algun evento de salir del programa
		for event in event_list:
	 	# Si se quiere salir, se le indica al director
			if event.type == pygame.QUIT:
				self.gameManager.program_exit()

		# # Indicamos la acción a realizar segun la tecla pulsada para cada jugador
		# teclasPulsadas = pygame.key.get_pressed()
		# self.jugador1.mover(teclasPulsadas, K_UP, K_DOWN, K_LEFT, K_RIGHT)
		# self.jugador2.mover(teclasPulsadas, K_w,  K_s,    K_a,    K_d)
		return
