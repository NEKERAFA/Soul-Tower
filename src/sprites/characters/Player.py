# -*- coding: utf-8 -*-

import pygame, sys, os
from pygame.locals import *
from src.sprites.Character import *
from src.sprites.characters.player.specials.Normal import *
from src.sprites.characters.player.specials.Dashing import *
from src.sprites.characters.player.specials.Defending import *
from src.sprites.characters.player.specials.Stunned import *
from src.sprites.characters.player.changing.Finish import *
from src.sprites.attacks.MeleeAttack import *
from src.sprites.attacks.RangedAttack import *
from src.controls.KeyboardMouseControl import *
from src.ResourceManager import *

# -------------------------------------------------
# -------------------------------------------------
# Constantes
# -------------------------------------------------
# -------------------------------------------------

PLAYER_SPEED = 0.2 # Pixeles por milisegundo
PLAYER_PATH = 'player'
SORCERER_PATH = os.path.join(PLAYER_PATH, 'sorcerer.png')
WARRIOR_PATH = os.path.join('sprites', 'characters', PLAYER_PATH, 'warrior.png')
PLAYER_CONF_PATH = os.path.join(PLAYER_PATH, 'info.json')

# -------------------------------------------------
# Clase del Character jugable
class Player(Character):
    def __init__(self, enemies, stage, loadStats=None):
        # Invocamos al constructor de la clase padre con la configuracion de este Character concreto
        Character.__init__(self, SORCERER_PATH, PLAYER_CONF_PATH, loadStats)

        # Cargamos las sprite sheets
        self.sorcererSheet = self.sheet.copy()
        self.warriorSheet = ResourceManager.load_image(WARRIOR_PATH, (-1))
        self.shield = ShieldSprite('shield.png', 'shield.json')

        # Coste de energía de los ataques
        self.rangedAttackEnergyCost = 1.5
        self.meleeAttackEnergyCost = 1

        # Radios y delays de ataques
        self.rangedAttackRadius = 1
        self.rangedAttackDelay = self.stats["rng_del"]
        self.meleeAttackRadius = 15
        self.meleeAttackDelay = self.stats["mel_del"]

        # Control de opciones escogidas en las ventanas mágicas
        #  Si se ha escogido alguna opción de sorceress O warrior
        self.choseAnythingNotShared = self.stats["chose_not_shared"]
        #  Si se ha escogido la opción 5
        self.killedFriend = self.stats["killed_friend"]
        #  Sumador de las opciones escogidas: cada opción de sorceress +1,
        #  cada opción de warrior -1. Si el número termina siendo 0 después de
        #  la tercera opción significa que se han escogido 3-1-2 o 3-2-1
        self.choiceAdder = self.stats["choice_adder"]

        # Guardo la fase actual
        self.stage = stage

        # Atributo de estado del jugador (patrón estado)
        self.state = Normal()

        # Número de almas
        self.souls = self.stats["souls"]

        # Inventario
        self.inventory = []

        # Esta variable mira si se puede cambiar de personaje o no
        self.canChange = True

        # Personaje activo en este momento
        self.currentCharacter = 'sorcerer'

        # Si se está cambiando de personaje o no
        self.changing = Finish()

        # Si se está utilizando el escudo o no
        self.usingShield = False

        #Se reservan 3 canales
        pygame.mixer.set_reserved(3)
        self.channel_heal = pygame.mixer.Channel(0)
        self.channel_damage = pygame.mixer.Channel(1)
        self.channel_souls = pygame.mixer.Channel(2)
        #Sonido para cuando se recupera vida
        self.heal_sound = ResourceManager.load_effect_sound("heal.ogg")

        #Sonido cuando se recive daño
        self.damage_sound = ResourceManager.load_effect_sound("ouch.ogg")

        #Sonido al recoger almas
        self.souls_sound = ResourceManager.load_effect_sound("soul_get.ogg")

        # Nivel de las armas
        self.meleeLevel = 1
        self.rangedLevel = 1

        # Se cargan los ataques
        self.attack = RangedAttack(self.rangedAttackRadius, self.rangedAttackDelay, self.rangedLevel, enemies)

    def move(self, viewport):
        # Indicamos la acción a realizar segun la tecla pulsada para el jugador
        if KeyboardMouseControl.left():
            if KeyboardMouseControl.up():
                Character.move(self, NW)
            elif KeyboardMouseControl.down():
                Character.move(self, SW)
            else:
                Character.move(self, W)
        elif KeyboardMouseControl.right():
            if KeyboardMouseControl.up():
                Character.move(self, NE)
            elif KeyboardMouseControl.down():
                Character.move(self, SE)
            else:
                Character.move(self, E)
        elif KeyboardMouseControl.up():
            Character.move(self, N)
        elif KeyboardMouseControl.down():
            Character.move(self, S)
        else:
            Character.move(self, STILL)

        # Control de ataque
        if KeyboardMouseControl.prim_button():
            # Si es sorcerer, el ataque actual es ataque a distancia
            if self.currentCharacter == 'sorcerer' and type(self.attack) is not RangedAttack:
                self.attack = RangedAttack(self.rangedAttackRadius, self.rangedAttackDelay, self.rangedLevel, self.attack.enemies)

            # Si es warrior, el ataque actual es melee
            if self.currentCharacter == 'warrior' and type(self.attack) is not MeleeAttack:
                self.attack = MeleeAttack(self.meleeAttackRadius, self.meleeAttackDelay, self.meleeLevel, self.attack.enemies)

            # Calcular la posición del centro del sprite (de momento calcula el centro del primer sprite)
            centerPosX, centerPosY = self.rect.center
            centerPosX -= viewport.left
            centerPosY -= viewport.top
            centerPos = centerPosX, centerPosY

            if(type(self.attack) is RangedAttack and self.stats["nrg"] >= self.rangedAttackEnergyCost and self.attack.elapsedTime >= self.rangedAttackDelay):
                self.add_energy(-self.rangedAttackEnergyCost)
                self.attack.start_attack(self.rect.center, KeyboardMouseControl.angle(centerPos))
            elif(type(self.attack) is MeleeAttack and self.stats["nrg"] >= self.meleeAttackEnergyCost and self.attack.elapsedTime >= self.meleeAttackDelay):
                self.add_energy(-self.meleeAttackEnergyCost)
                self.attack.start_attack(self.rect.center, KeyboardMouseControl.angle(centerPos))
            else:
                self.attack.end_attack()

        # Finalizamos el ataque
        else:
            self.attack.end_attack()

    def update(self, time, stage):
        # Ataque especial
        if KeyboardMouseControl.sec_button():
            # Si es sorcerer el jugador actual, cambiamos el estado a dashing
            if self.currentCharacter == 'sorcerer' and type(self.state) is not Dashing:
                self.state.change(self, Dashing)
            # Si es warrior el jugador actual, cambiamos el estado a defending
            if self.currentCharacter == 'warrior' and (type(self.state) is not Defending and type(self.state) is not Stunned):
                self.state.change(self, Defending)
        else:
            if self.currentCharacter == 'warrior' and type(self.state) is not Stunned:
                self.state.change(self, Normal)

        # Controlamos el cambio de personaje
        self.changing.update(self, time, stage)

    def draw(self, screen):
        # Esta función está para agrupar el mostrar al jugador y su ataque
        screen.blit(self.image, self.rect)
        if self.usingShield:
            screen.blit(self.shield.image, self.shield.rect)
        self.attack.draw(screen)

    ############################################################################

    # Llama a la interfaz a actualizar la cantidad de almas
    def update_souls(self):
        self.stage.gui.soulsText.change_text(str(self.souls))

    # Incrementa el número de almas del jugador
    def increase_souls(self, souls):
        self.channel_souls.play(self.souls_sound)
        self.stats["souls"] += souls
        self.souls += souls
        # Actualizo la GUI
        self.update_souls()

    # Decrementa el número de almas del jugador
    def decrement_souls(self, souls):
        self.souls -= souls
        # Actualizo la GUI
        self.update_souls()

    # Recibe un daño y se realiza el daño. Si el personaje ha muerto, lo elimina
    # de todos los grupos
    def receive_damage(self, damage, force):
        self.channel_damage.play(self.damage_sound)
        life = self.stats["hp"]
        self.state.receive_damage(self, damage, force)
        remainLife = self.stats["hp"]
        # Actualizo la GUI
        for i in range(0, life-remainLife):
            self.stage.gui.health.lose_life()

    # Añade vidas al personaje
    def add_lifes(self, lifes):
        self.channel_heal.play(self.heal_sound)
        life = self.stats["hp"]
        Character.add_lifes(self, lifes)
        remainLife = self.stats["hp"]
        # Actualizo la GUI
        for i in range(0, remainLife-life):
            self.stage.gui.health.gain_life()

    # Añade vida máxima al personaje
    # Cuando esto suceda, la vida se regenera por completo
    def add_max_life(self):
        self.stats["max_hp"] += 1
        self.stats["hp"] = self.stats["max_hp"]
        self.stage.gui.health.gain_max_life()

    # Añadir (o disminuír) energía
    def add_energy(self, value):
        self.stats["nrg"] += value
        if(self.stats["nrg"]>self.stats["max_nrg"]):
            self.stats["nrg"] = self.stats["max_nrg"]
        elif(self.stats["nrg"]<0):
            self.stats["nrg"] = 0
        self.stage.gui.energy.set_energy(self.stats["nrg"])

    # Fijar energía a un valor
    def set_energy(self, value):
        self.stats["nrg"] = value
        #if(self.stats["nrg"]>self.stats["max_nrg"]):
        #    self.stats["nrg"] = self.stats["max_nrg"]
        #elif(self.stats["nrg"]<0):
        #    self.stats["nrg"] = 0

        self.stage.gui.energy.set_energy(self.stats["nrg"])

    # Añade energía máxima al personaje
    # Cuando esto suceda, la energía se regenera por completo
    def add_max_energy(self):
        self.stats["max_nrg"] += 1
        self.stats["nrg"] = self.stats["max_nrg"]
        self.stage.gui.energy.gain_energy_bar()

    # Añade nuevos enemigos en el cambio de fase
    def set_enemies(self, enemies):
        self.attack.enemies = enemies

    # Cambia de fase al jugador
    def change_stage(self, stage):
        self.stage = stage

    # TODO pal UML
    def change_character(self):
        self.canChange = False
        #TODO: esta línea es un cáncer pero tampoco sé cómo ponerla bien
        self.stage.gui.charSymb.action()
        # Ponemos la posición de parado
        Character.move(self, STILL)

        # Cogemos el rectángulo de vista frontal
        currentRect = self.sheetConf[0][0]['coords']
        # Actualizamos el sprite con el nuevo sprite sheet
        self.origImage = self.sheet.subsurface(currentRect)
        # Actualizamos el sprite que se dibuja
        self.image = self.origImage.copy()
        # Actualizamos el delay
        self.changing.currentDelay = self.sheetConf[0][0]['delay']

        # Cambiamos de estado
        self.changing = Fadein(self.origImage.get_width(), self.canChange)
