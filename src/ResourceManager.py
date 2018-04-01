# -*- coding: utf-8 -*-

import pygame, sys, os, json
from pygame.locals import *

IMAGE_PATH = os.path.join('assets', 'images')
SPRITE_SHEET_PATH = os.path.join('assets', 'sprites')
STAGE_CONF_PATH = os.path.join('assets', 'stages')
ROOM_CONF_PATH = os.path.join('assets', 'rooms')
DIALOGUE_CONF_PATH = os.path.join('assets', 'dialogues')
FONT_PATH = os.path.join('assets', 'fonts')

# -------------------------------------------------
# Clase ResourceManager

# En este caso se implementa como una clase vacía, solo con métodos de clase
class ResourceManager(object):
    resources = {}


    @classmethod
    def load_music(cls, name):
        #Si ya está presente en los resources
        if name in cls.resources:
            #Se devuelve de los recursos
            return cls.resources[name]
        #Si no se cargó anteriormente
        else:
            fullname = os.path.join('assets', 'sounds', 'music', name)
            try:
                music=pygame.mixer.music.load(fullname)
            except pygame.error, message:
                print 'Cannot load music file: ', fullname
                raise SystemExit, message
            #Se almacena
            cls.resources[name] = music
            return music


    @classmethod
    def load_effect_sound(cls, name):
        if name in cls.resources:
            return cls.resources[name]
        else:
            fullname = os.path.join('assets/sounds/effects', name)
            try:
                sound_effect=pygame.mixer.Sound(fullname)
                #sound_effect.set_volume(0.7);
                print(fullname)
                print(sound_effect.get_volume())
            except pygame.error, message:
                print 'Cannot load sound effect file:', fullname
                raise SystemExit, message
            #Se almacena
            cls.resources[name] = sound_effect
            return sound_effect


    @classmethod
    def load_image(cls, name, colorkey=None):
        fullname = os.path.join(IMAGE_PATH, name)
        # Si el name de archivo está entre los resources ya cargados
        if fullname in cls.resources:
            # Se devuelve ese recurso
            return cls.resources[fullname]
        # Si no ha sido cargado anteriormente
        else:
            # Se carga la imagen indicando la carpeta en la que está
            try:
                image = pygame.image.load(fullname)
            except pygame.error, message:
                print 'Cannot load image:', fullname
                raise SystemExit, message

            # Obtenemos el colorkey
            if colorkey is not None:
                if colorkey is -1:
                    colorkey = image.get_at((0,0))
                image.set_colorkey(colorkey, RLEACCEL)

            # Convertimos el canal alpha
            image = image.convert_alpha()

            # Se almacena
            cls.resources[fullname] = image
            # Se devuelve
            return image

    @classmethod
    def free_image(cls, name):
        fullname = os.path.join(IMAGE_PATH, name)
        if fullname in cls.resources:
            del cls.resources[fullname]

    @classmethod
    def load_sprite_conf(cls, name):
        fullname = os.path.join(SPRITE_SHEET_PATH, name)
        # Si el name de archivo está entre los resources ya cargados
        if fullname in cls.resources:
            # Se devuelve ese recurso
            return cls.resources[fullname]
        # Si no ha sido cargado anteriormente
        else:
            # Se carga el recurso indicando el name de su carpeta
            try:
                pfile = open(fullname, 'r')
            except IOError as e:
                print 'Cannot load sprite sheet:', fullname
                raise SystemExit, e.strerror
            # Se carga y parsea el json
            data = json.load(pfile)
            pfile.close()
            # Se almacena
            cls.resources[fullname] = data
            # Se devuelve
            return data

    @classmethod
    def free_sprite_conf(cls, name):
        fullname = os.path.join(SPRITE_SHEET_PATH, name)
        if fullname in cls.resources:
            del cls.resources[fullname]

    @classmethod
    def load_room(cls, name):
        fullname = os.path.join(ROOM_CONF_PATH, name)
        # Si el name de archivo está entre los resources ya cargados
        if fullname in cls.resources:
            # Se devuelve ese recurso
            return cls.resources[fullname]
        # Si no ha sido cargado anteriormente
        else:
            # Se carga el recurso indicando el name de su carpeta
            try:
                pfile = open(fullname, 'r')
            except IOError as e:
                print 'Cannot load room:', fullname
                raise SystemExit, e.strerror
            data = json.load(pfile)
            pfile.close()
            # Se almacena
            cls.resources[fullname] = data
            # Se devuelve
            return data

    @classmethod
    def free_room(cls, name):
        fullname = os.path.join(ROOM_CONF_PATH, name)
        if fullname in cls.resources:
            del cls.resources[fullname]

    @classmethod
    def load_stage(cls, name):
        fullname = os.path.join(STAGE_CONF_PATH, name)
        # Si el name de archivo está entre los resources ya cargados
        if fullname in cls.resources:
            # Se devuelve ese recurso
            return cls.resources[fullname]
        # Si no ha sido cargado anteriormente
        else:
            # Se carga el recurso indicando el name de su carpeta
            try:
                pfile = open(fullname, 'r')
            except IOError as e:
                print 'Cannot load stage:', fullname
                raise SystemExit, e.strerror
            data = json.load(pfile)
            pfile.close()
            # Se almacena
            cls.resources[fullname] = data
            # Se devuelve
            return data

    @classmethod
    def fre_stage(cls, name):
        fullname = os.path.join(STAGE_CONF_PATH, name)
        if fullname in cls.resources:
            del cls.resources[fullname]

    @classmethod
    def load_dialogue(cls, name):
        fullname = os.path.join(DIALOGUE_CONF_PATH, name)
        # Si el name de archivo está entre los resources ya cargados
        if fullname in cls.resources:
            # Se devuelve ese recurso
            return cls.resources[fullname]
        # Si no ha sido cargado anteriormente
        else:
            try:
                pfile = open(fullname, 'r')
            except IOError as e:
                print 'Cannot load dialogue:', fullname
                raise SystemExit, e.strerror
            data = json.load(pfile)
            pfile.close()
            # Se almacena
            cls.resources[fullname] = data
            # Se devuelve
            return data

    @classmethod
    def free_dialogue(cls, name):
        fullname = os.path.join(DIALOGUE_CONF_PATH, name)
        if fullname in cls.resources:
            del cls.resources[fullname]

    @classmethod
    def load_font(cls, name, size):
        fullname = os.path.join(FONT_PATH, name)
        if (fullname, size) in cls.resources:
            return cls.resources[(fullname, size)]
        else:
            try:
                font = pygame.font.Font(fullname, size)
            except pygame.error, message:
                print 'Cannot load font:', fullname
                raise SystemExit, message

            cls.resources[(fullname, size)] = font

            return font

    @classmethod
    def free_font(cls, name, size):
        fullname = os.path.join(FONT_PATH, name)
        if (fullname, size) in cls.resources:
            del cls.resources[(fullname, size)]
