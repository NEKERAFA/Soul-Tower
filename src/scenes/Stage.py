# -*- coding: utf-8 -*-

import pygame, string
from src.ResourceManager import *
from src.scenes.Scene import *
from src.scenes.screens.Room import *
from src.sprites.Player import *
from src.sprites.Enemy import *

# -------------------------------------------------
# Clase Stage

SCREEN_CENTER_X = int(SCREEN_WIDTH / 2)

class Stage(Scene):
    def __init__(self, stageFile, gameManager):
        # Primero invocamos al constructor de la clase padre
        Scene.__init__(self, gameManager)

        # Cargamos la configuración del nivel
        data = ResourceManager.load_stage(stageFile)

        # Cargamos las rutas de las salas
        images = os.listdir("assets/images/rooms/" + data["path"])
        images.sort(key=string.lower)
        configs = os.listdir("assets/rooms/" + data["path"])
        configs.sort(key=string.lower)

        if len(configs)*2 != len(images):
            raise SystemExit, "Los archivos de imagenes y configuración no guardan relación"

        # Cargamos las salas
        pth_img = "rooms/" + data["path"] + "/"
        pth = data["path"] + "/"
        self.rooms = [Room(pth_img + images[i*2], pth_img + images[i*2+1], pth + configs[i]) for i in range(0, len(configs))]
        self.currentRoom = 0

        # Cargamos el sprite del jugador
        self.player = Player()
        self.player.change_global_position((data["player_pos"][0], data["player_pos"][1]))
    # ----------- Añadido para probar colisiones
        self.enemy = Enemy('characters/sorcerer.png', 'sorcerer.json')
        self.enemy.change_global_position((data["player_pos"][0], data["player_pos"][1]))
        self.spritesGroup = pygame.sprite.Group(self.player, self.enemy)
    # -----------

        # Calculamos el scroll inicial
        #self.scroll = ((self.player.position[0] + self.player.offset[0]) - self.rooms[self.currentRoom].x, (self.player.position[1] + self.player.offset[1]) - self.rooms[self.currentRoom].y)
        self.scroll = (0,0)

        # TODO añadido Iniciamos el viewport
        self.viewport = gameManager.screen.get_rect()
        self.viewport.center = self.player.rect.center
        self.viewport.clamp_ip(self.rooms[self.currentRoom].rect)

    def update(self, time):
        # Actualizamos los sprites
        self.spritesGroup.update(self.rooms[self.currentRoom], time) # TODO pasar la máscara

        # Actualizamos el scroll
        # self.updateScroll()

    def events(self, events):
        # Miramos a ver si hay algun evento de salir del programa
        for event in events:
            # Si se quiere salir, se le indica al director
            if event.type == pygame.QUIT:
                self.gameManager.program_exit()
                return
        # Indicamos la acción a realizar para el jugador
        self.player.move()

    def draw(self, screen):
        # Muestro un color de fondo
        screen.fill((100, 200, 255))
        room = self.rooms[self.currentRoom]
        # Imprimo la escena
        room.draw(screen)
        # Luego los Sprites
        self.spritesGroup.draw(screen)
        self.player.melee_manager.draw(screen)
        # ------ Colisiones melee
        if (self.player.melee_manager.animating):
            atk_mask = pygame.mask.from_surface(self.player.melee_manager.image)
            enemy_mask = pygame.mask.from_surface(self.enemy.image)
            (atk_pos_x, atk_pos_y) = self.player.melee_manager.position
            (enemy_pos_x, enemy_pos_y) = self.enemy.position
            enemy_pos_y -= self.enemy.sheetConf[0][0]['coords'][3]
            offset = (int(enemy_pos_x - atk_pos_x), int(enemy_pos_y - atk_pos_y))
            collision = atk_mask.overlap(enemy_mask, offset)
        #     if collision is not None:
        #         # print(atk_pos_x,atk_pos_y,' - ', enemy_pos_x, enemy_pos_y)
        #         # print(offset)
        # # ------
        # # # TODO nuevo
        # # def updateScroll(self):
        # #     self.viewport.center = self.player.rect.center
        # #     self.viewport.clamp_ip(self.rooms[self.currentRoom].rect)
