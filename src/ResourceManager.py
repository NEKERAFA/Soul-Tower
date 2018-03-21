# -*- coding: utf-8 -*-

import pygame, sys, os, json
from pygame.locals import *

# -------------------------------------------------
# Clase ResourceManager

# En este caso se implementa como una clase vacía, solo con métodos de clase
class ResourceManager(object):
    resources = {}

    @classmethod
    def load_image(cls, name, colorkey=None):
        # Si el name de archivo está entre los resources ya cargados
        if name in cls.resources:
            # Se devuelve ese recurso
            return cls.resources[name]
        # Si no ha sido cargado anteriormente
        else:
            # Se carga la imagen indicando la carpeta en la que está
            fullname = os.path.join('assets', 'images', name)
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
            cls.resources[name] = image
            # Se devuelve
            return image

    @classmethod
    def load_sprite_conf(cls, name):
        # Si el name de archivo está entre los resources ya cargados
        if name in cls.resources:
            # Se devuelve ese recurso
            return cls.resources[name]
        # Si no ha sido cargado anteriormente
        else:
            # Se carga el recurso indicando el name de su carpeta
            fullname = os.path.join('assets', 'sprites', name)
            pfile = None
            try:
                pfile = open(fullname, 'r')
            except IOError as e:
                print 'Cannot load sprite sheet:', fullname
                raise SystemExit, e.strerror
            # Se carga y parsea el json
            data = json.load(pfile)
            pfile.close()
            # Se almacena
            cls.resources[name] = data
            # Se devuelve
            return data

    @classmethod
    def load_room(cls, name):
        # Si el name de archivo está entre los resources ya cargados
        if name in cls.resources:
            # Se devuelve ese recurso
            return cls.resources[name]
        # Si no ha sido cargado anteriormente
        else:
            # Se carga el recurso indicando el name de su carpeta
            fullname = os.path.join('assets', 'rooms', name)
            pfile = None
            try:
                pfile = open(fullname, 'r')
            except IOError as e:
                print 'Cannot load room:', fullname
                raise SystemExit, e.strerror
            data = json.load(pfile)
            pfile.close()
            # Se almacena
            cls.resources[name] = data
            # Se devuelve
            return data

    @classmethod
    def load_stage(cls, name):
        # Si el name de archivo está entre los resources ya cargados
        if name in cls.resources:
            # Se devuelve ese recurso
            return cls.resources[name]
        # Si no ha sido cargado anteriormente
        else:
            # Se carga el recurso indicando el name de su carpeta
            fullname = os.path.join('assets', 'stages', name)
            pfile = None
            try:
                pfile = open(fullname, 'r')
            except IOError as e:
                print 'Cannot load stage:', fullname
                raise SystemExit, e.strerror
            data = json.load(pfile)
            pfile.close()
            # Se almacena
            cls.resources[name] = data
            # Se devuelve
            return data

    @classmethod
    def load_dialogue(cls, name):
        # Si el name de archivo está entre los resources ya cargados
        if name in cls.resources:
            # Se devuelve ese recurso
            return cls.resources[name]
        # Si no ha sido cargado anteriormente
        else:
            # Se carga el recurso indicando el name de su carpeta
            fullname = os.path.join('assets', 'dialogues', name)
            pfile = None
            try:
                pfile = open(fullname, 'r')
            except IOError as e:
                print 'Cannot load dialogue:', fullname
                raise SystemExit, e.strerror
            data = json.load(pfile)
            pfile.close()
            # Se almacena
            cls.resources[name] = data
            # Se devuelve
            return data

    @classmethod
    def load_font(cls, name, size):
        if (name, size) in cls.resources:
            return cls.resources[(name, size)]
        else:
            fullname = os.path.join('assets', 'fonts', name)
            font = None
            try:
                font = pygame.font.Font(fullname, size)
            except pygame.error, message:
                print 'Cannot load font:', fullname
                raise SystemExit, message

            cls.resources[(name, size)] = font

            return font
