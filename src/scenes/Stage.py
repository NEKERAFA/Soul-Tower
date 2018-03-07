# -*- coding: utf-8 -*-

import pygame, string
from src.ResourceManager import *
from src.scenes.Scene import *
from src.scenes.screens.Room import *
from src.sprites.Player import *

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
        self.spritesGroup = pygame.sprite.Group(self.player)

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
        self.updateScroll()

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

    # TODO nuevo
    def updateScroll(self):
        self.viewport.center = self.player.rect.center
        self.viewport.clamp_ip(self.rooms[self.currentRoom].rect)

    # TODO notas:
    """
    self.screen = pg.display.getSurface() <- pantalla
    self.screen_rect = self.screen.get_rect() <- rectángulo de la pantalla
    Este rectángulo se le pasaría a Stage en el constructor (viewport):
    self.image = imagen del mapa
    self.mask <- en principio si la detección de colisión se hace fuera aquí nada
    self.rect = self.image.get_rect()
    self.player
    self.player.rect.center = self.rect.center
    self.viewport

    En update_viewport de Stage:
    self.viewport.center = self.player.rect.center
    self.viewport.clamp_ip(self.rect)

    En update de Stage:
    self.player.update(self.mask, keys)
    self.update_viewport()

    En draw de Stage:
    new_image = self.image.copy()
    self.player.draw(new_image)
    surface.fill([whatever])
    surface.blit(new_image, (0,0), self.viewport)

    """

    # def updateScroll(self, player):
    #     changeScroll = False
    #     leftLimit = self.rooms[self.currentRoom].x + SCREEN_CENTER_X
    #     rightLimit = self.rooms[self.currentRoom].x + self.rooms[self.currentRoom].width - SCREEN_CENTER_X
    #     playerCenter = player.position[0] + player.offset[0]
    #     lastScrollX = self.scroll[0] + self.rooms[self.currentRoom].x + SCREEN_CENTER_X
    #
    #     scrollX = self.scroll[0]
    #
    #     # Si el personaje se ha movido hacia la izquierda
    #     if (player.movement == W) or (player.movement == NW) or (player.movement == SW):
    #         # Si el personaje está fuera de la zona derecha en la que no se hace scroll
    #         if lastScrollX <= rightLimit:
    #             # Si el escenario ya está a la izquierda del todo, no lo movemos más, pero actualizamos el scroll
    #             if lastScrollX - SCREEN_CENTER_X <= self.rooms[self.currentRoom].x:
    #                 scrollX = (player.position[0] + player.offset[0]) - self.rooms[self.currentRoom].x - SCREEN_CENTER_X # El scroll en x se corresponde con la distancia de la coordenada x del centro del personaje al borde izquierdo de la sala
    #
    #             # Si se puede hacer scroll a la izquierda
    #             else:
    #                 scrollX = (player.position[0] + player.offset[0]) - self.rooms[self.currentRoom].x - SCREEN_CENTER_X
    #                 changeScroll = True
    #
    #     # Si el personaje se ha movido hacia la derecha
    #     if (player.movement == E) or (player.movement == NE) or (player.movement == SE):
    #         # Si el personaje está fuera de la zona izquierda en la que no se hace scroll
    #         if lastScrollX >= leftLimit:
    #             scrollX = playerCenter - self.rooms[self.currentRoom].x - SCREEN_CENTER_X
    #             # Si el escenario ya está a la derecha del todo, no lo movemos más
    #             if lastScrollX < rightLimit:
    #                 changeScroll = True
    #         else:
    #             scroll = SCREEN_CENTER_X
    #
    #     #scrollX =   - self.rooms[self.currentRoom].x - SCREEN_CENTER_X # Si se comenta esta línea no va :3
    #     self.scroll = (scrollX, self.scroll[1])
    #     # Si se cambió el scroll, se desplazan todos los Sprites y el decorado
    #     if changeScroll:
    #         # Actualizamos la posición en pantalla de todos los Sprites según el scroll actual
    #         for sprite in iter(self.spritesGroup):
    #             sprite.change_screen_position(self.scroll)
    #
    #         # Además, actualizamos la sala para que se muestre una parte distinta
    #         self.rooms[self.currentRoom].update(self.scroll)
