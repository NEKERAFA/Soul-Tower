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
from src.scenes.stage.InRoomState import *
from src.scenes.stage.SmallRoomState import *
from src.interface.screens.GUIPlayerScreen import *
from src.interface.screens.GUIWindowDialogScreen import *
from src.interface.screens.GUIGameOverScreen import *
from src.interface.screens.GUICreditsScreen import *

# -------------------------------------------------
# Clase Stage

SCREEN_CENTER_X = int(SCREEN_WIDTH/2)

class Stage(Scene):
    inRoomState = InRoomState()
    smallRoomState = SmallRoomState()

    def __init__(self, stageNum, gameManager, player=None, playerStats=None):
        # Primero invocamos al constructor de la clase padre
        Scene.__init__(self, gameManager)

        self.stageNum = int(stageNum)

        # Obtenemos el nombre de la fase
        fullname = 'stage_' + str(int(stageNum))

        # Cargamos la imagen
        image_path = os.path.join('stages', fullname + '.png')
        self.image = ResourceManager.load_image(image_path)

        # Cargamos las máscaras
        maskPath = os.path.join('stages', fullname + '_mask.png')
        maskImage = ResourceManager.load_image(maskPath, (0, 0, 0))
        self.mask = pygame.mask.from_surface(maskImage)
        rangedMaskPath = os.path.join('stages', fullname + '_rangedMask.png')
        rangedMaskImage = ResourceManager.load_image(rangedMaskPath, (0, 0, 0))
        self.rangedMask = pygame.mask.from_surface(rangedMaskImage)

        # Cargamos la configuración del nivel
        data = ResourceManager.load_stage(fullname + '.json')

        # Cargamos la musica
        self.bgmFile = data["music"]

        # Cargamos las salas
        self.rooms = []
        for i in range(0, data["rooms"]):
            self.rooms.append(Room(stageNum, i, self))

        # Metemos las llaves en su sitio
        for room in self.rooms:
            for door in room.unlockedDoors:
                if hasattr(door, 'key') and door.key is not None:
                    door.key = self.rooms[door.key[0]].keys[door.key[1]]

        self.currentRoom = 0

        # Lista de enemigos
        enemies = [enemy for room in self.rooms for enemy in room.enemies.sprites()]
        enemiesGroup = pygame.sprite.Group(enemies)

        # Cargamos el sprite del jugador
        if player is None:
            self.player = Player(enemiesGroup, self, playerStats)
        else:
            self.player = player
            self.player.set_enemies(enemiesGroup)
        # Lo ponemos en su posición final
        if(playerStats is not None):
            self.player.change_global_position((playerStats["player_pos"][0], playerStats["player_pos"][1]))
        else:
            self.player.change_global_position((data["player_pos"][0], data["player_pos"][1]))

        self.saveData = None
        self.save_data(data)

        # Cargamos la interfaz del jugador
        # TODO: meter datos de la interfaz en json, y hacerlo dependiente de la sala en la que se encuentre el jugador
        self.gui = GUIPlayerScreen(self)

        # Diálogo de ventana
        self.guiWindow = None
        #self.create_window_dialog(None)

        # Pantalla de game over
        self.guiGameOver = None

        # Pantalla de créditos
        self.guiCredits = None
        #self.guiCredits = GUICreditsScreen(self)

        # Inicializamos el viewport, que es un rectángulo del tamaño de la
        # pantalla que indicará qué porción de la sala se debe mostrar
        self.viewport = gameManager.screen.get_rect()
        self.viewport.center = self.player.rect.center
        self.viewport.clamp_ip(self.rooms[self.currentRoom].rect)

        # Empezamos en estado de entrar en sala
        self.state = OnEnterState()

    def update(self, time):

        if not self.player.killed:
            # Delegamos en el estado la actualización de la fase
            self.state.update(time, self)
        elif (self.guiGameOver is None):
            self.guiGameOver = GUIGameOverScreen(self)
        else:
            self.guiGameOver.update(time)

    def events(self, events):
        # Miramos a ver si hay algun evento de salir del programa
        for event in events:
            # Si se quiere salir, se le indica al director
            if event.type == pygame.QUIT:
                self.gameManager.program_exit()
                return
        if(self.guiGameOver is not None):
            self.guiGameOver.events(events)
        # Delegamos en el estado la acción a realizar para el Jugador
        self.state.events(events, self)

        #if(self.guiWindow is not None):
        #    self.guiWindow.events(events)

    def draw(self, screen):
        # Delegamos en el estado el dibujado de la fase
        self.state.draw(screen, self)
        #TODO: gui debería estar en un array, como Rooms

        if(self.guiWindow is not None):
            self.guiWindow.draw(screen)
        if(self.guiGameOver is not None):
            self.guiGameOver.draw(screen)

    # Cambia el estado que controla el comportamiento del scroll
    def set_state(self, state):
        self.state = state

    # Reproduce la música del nivel
    def play_bgm(self):
        ResourceManager.load_music(self.bgmFile)
        pygame.mixer.music.play(-1, 0.0)

    # Crear diálogo para las ventanas
    def create_window_dialog(self, selectionFile):
        self.guiWindow = GUIWindowDialogScreen(self, selectionFile)
        return self.guiWindow

     # Eliminar diálogo para ventanas
    def remove_window_dialog(self):
        self.guiWindow = None

    # Crea la fase siguiente
    def next_stage(self):
        return Stage(self.stageNum+1, self.gameManager, self.player)

    # Creo de nuevo la fase
    def new_stage(self, data):
        return Stage(self.stageNum, self.gameManager, None, data)

    # Guardo los datos del juego
    def save_data(self, data):
        self.savedData = self.player.stats.copy()
        self.savedData["player_pos"] = (data["player_pos"][0], data["player_pos"][1])
        self.savedData["rng_del"] = self.player.rangedAttackDelay
        self.savedData["mel_del"] = self.player.meleeAttackDelay

        self.savedData["chose_not_shared"] = self.player.choseAnythingNotShared
        self.savedData["killed_friend"] = self.player.killedFriend
        self.savedData["choice_adder"] = self.player.choiceAdder

        self.savedData["souls"] = self.player.souls
