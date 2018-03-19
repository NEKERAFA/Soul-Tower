# -*- coding: utf-8 -*-

import pygame, string, os
from src.ResourceManager import *
from src.scenes.Scene import *
from src.scenes.screens.Room import *
from src.sprites.Player import *
from src.scenes.InRoomState import *
from src.scenes.SmallRoomState import *
from src.sprites.Enemy import *

# -------------------------------------------------
# Clase Stage

SCREEN_CENTER_X = int(SCREEN_WIDTH / 2)

class Stage(Scene):

    inRoomState = InRoomState()
    smallRoomState = SmallRoomState()

    def __init__(self, stageFile, gameManager):
        # Primero invocamos al constructor de la clase padre
        Scene.__init__(self, gameManager)

        # Cargamos la configuración del nivel
        data = ResourceManager.load_stage(stageFile)

        image_path = os.path.join('stages', data["image"])
        self.image = ResourceManager.load_image(image_path, (255, 0, 255))
        self.image.convert_alpha()
        mask_path = os.path.join('stages', data["mask"])
        mask_image = ResourceManager.load_image(mask_path, (-1))
        self.mask = pygame.mask.from_surface(mask_image)

        # Cargamos las rutas de las salas
        configs = os.listdir("assets/rooms/" + data["path"])
        configs.sort(key=string.lower)

        # Cargamos las salas
        pth = data["path"] + "/"
        self.rooms = [Room(pth + configs[i]) for i in range(0, len(configs))]
        self.currentRoom = 0

        # Cargamos el sprite del jugador
        self.enemies = []

        self.player = Player(self.enemies, self)
        self.player.change_global_position((data["player_pos"][0], data["player_pos"][1]))

    # ----------- Añadido para probar colisiones
        self.enemy = Enemy('characters/sorcerer.png', 'sorcerer.json')
        self.enemy.change_global_position((data["player_pos"][0]+100, data["player_pos"][1]+100))
        self.enemies.append(self.enemy)
        self.spritesGroup = pygame.sprite.Group(self.player, self.enemy)
    # -----------

        self.bulletGroup = pygame.sprite.Group()

        # Inicializamos el viewport, que es un rectángulo del tamaño de la pantalla
        # que indicará qué porción de la sala se debe mostrar
        self.viewport = gameManager.screen.get_rect()
        self.viewport.center = self.player.rect.center
        self.viewport.clamp_ip(self.rooms[self.currentRoom].rect)

        # Empezamos en estado de dentro de sala
        self.state = Stage.inRoomState

        # TODO DEBUG: BORRAR CUANDO HAGA FALTA
        self.font = pygame.font.Font(None, 16)
        self.posPlayer = self.font.render("x: " + str(int(self.player.position[0])) + ", y: " + str(int(self.player.position[1])), True, (0, 0, 0))
        self.posRoom = self.font.render("x: " + str(self.rooms[self.currentRoom].position[0]) + ", y: " + str(self.rooms[self.currentRoom].position[1]), True, (0, 0, 0))
        # TODO DEBUG: BORRAR CUANDO HAGA FALTA

    def update(self, time):
        # Delegamos en el estado la actualización de la fase
        self.state.update(time, self)

        # TODO DEBUG: BORRAR CUANDO HAGA FALTA
        self.posPlayer = self.font.render("x: " + str(int(self.player.position[0])) + ", y: " + str(int(self.player.position[1])), True, (0, 0, 0))
        self.posRoom = self.font.render("x: " + str(self.rooms[self.currentRoom].position[0]) + ", y: " + str(self.rooms[self.currentRoom].position[1]), True, (0, 0, 0))
        # TODO DEBUG: BORRAR CUANDO HAGA FALTA

    def events(self, events):
        # Miramos a ver si hay algun evento de salir del programa
        for event in events:
            # Si se quiere salir, se le indica al director
            if event.type == pygame.QUIT:
                self.gameManager.program_exit()
                return

        # Delegamos en el estado la acción a realizar para el Jugador
        self.state.events(events, self)

    def draw(self, screen):
        # Delegamos en el estado el dibujado de la fase
        self.state.draw(screen, self)
        # self.player.meleeAttack.draw(screen)
        # self.player.rangedAttack.draw(screen)

        # TODO DEBUG: BORRAR CUANDO HAGA FALTA
        screen.blit(self.posPlayer, (0, 0))
        screen.blit(self.posRoom, (0, 16))
        # TODO DEBUG: BORRAR CUANDO HAGA FALTA

    # Cambia el estado que controla el comportamiento del scroll
    def setState(self, state):
        self.state = state
