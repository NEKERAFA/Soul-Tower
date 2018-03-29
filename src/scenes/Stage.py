# -*- coding: utf-8 -*-

import pygame, string, os
from src.ResourceManager import *

from src.sprites.characters.Player import *
from src.sprites.characters.Enemy import *

from src.scenes.Scene import *
from src.scenes.stage.Room import *
from src.sprites.Character import *
from src.sprites.characters.Player import *
from src.scenes.stage.OnEnterState import *
from src.scenes.stage.OnLeaveState import *
from src.scenes.stage.InRoomState import *
from src.scenes.stage.SmallRoomState import *
from src.interface.screens.GUIPlayerScreen import *
from src.interface.screens.GUIWindowDialogScreen import *

# -------------------------------------------------
# Clase Stage

SCREEN_CENTER_X = int(SCREEN_WIDTH/2)

class Stage(Scene):
    inRoomState = InRoomState()
    smallRoomState = SmallRoomState()

    def __init__(self, stageNum, gameManager, player=None):
        # Primero invocamos al constructor de la clase padre
        Scene.__init__(self, gameManager)

        self.stageNum = int(stageNum)

        # Obtenemos el nombre de la fase
        fullname = 'stage_' + str(int(stageNum))

        # Cargamos la imagen
        image_path = os.path.join('stages', fullname + '.png')
        self.image = ResourceManager.load_image(image_path)

        # Cargamos la máscara
        mask_path = os.path.join('stages', fullname + '_mask.png')
        mask_image = ResourceManager.load_image(mask_path, (0, 0, 0))
        self.mask = pygame.mask.from_surface(mask_image)

        # Cargamos la configuración del nivel
        data = ResourceManager.load_stage(fullname + '.json')

        # Cargamos las salas
        self.rooms = []
        for i in range(0, data["rooms"]):
            self.rooms.append(Room(stageNum, i, self))
        self.currentRoom = 0

        # Lista de enemigos
        enemies = [enemy for room in self.rooms for enemy in room.enemies.sprites()]
        enemiesGroup = pygame.sprite.Group(enemies)

        # Cargamos el sprite del jugador
        if player is None:
            self.player = Player(enemiesGroup, self)
        else:
            self.player = player
        # Lo ponemos en su posición final
        self.player.change_global_position((data["player_pos"][0], data["player_pos"][1]))

        # Cargamos la interfaz del jugador
        # TODO: meter datos de la interfaz en json, y hacerlo dependiente de la sala en la que se encuentre el jugador
        self.gui = GUIPlayerScreen(self)

        # Diálogo de ventana
        self.guiWindow = None
        #self.create_window_dialog()

        # Inicializamos el viewport, que es un rectángulo del tamaño de la
        # pantalla que indicará qué porción de la sala se debe mostrar
        self.viewport = gameManager.screen.get_rect()
        self.viewport.center = self.player.rect.center
        self.viewport.clamp_ip(self.rooms[self.currentRoom].rect)

        # Empezamos en estado de entrar en sala
        self.state = OnEnterState()

        # Variable que nos dice si el boss ha muerto
        self.bossKilled = False

    def update(self, time):
        # Delegamos en el estado la actualización de la fase
        self.state.update(time, self)
        self.gui.update(time)
        if(self.guiWindow is not None):
            self.guiWindow.update(time)

    def events(self, events):
        # Miramos a ver si hay algun evento de salir del programa
        for event in events:
            # Si se quiere salir, se le indica al director
            if event.type == pygame.QUIT:
                self.gameManager.program_exit()
                return

        # Delegamos en el estado la acción a realizar para el Jugador
        self.state.events(events, self)
        self.gui.events(events)
        if(self.guiWindow is not None):
            self.guiWindow.events(events)

    def draw(self, screen):
        # Delegamos en el estado el dibujado de la fase
        self.state.draw(screen, self)
        #TODO: gui debería estar en un array, como Rooms
        self.gui.draw(screen)
        if(self.guiWindow is not None):
            self.guiWindow.draw(screen)

    # Cambia el estado que controla el comportamiento del scroll
    def set_state(self, state):
        self.state = state

    # Crear diálogo para las ventanas
    def create_window_dialog(self, selectionFile):
        self.guiWindow = GUIWindowDialogScreen(self, selectionFile)
        return self.guiWindow

     # Eliminar diálogo para ventanas
    def remove_window_dialog(self):
        self.guiWindow = None
