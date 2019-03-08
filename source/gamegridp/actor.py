# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 21:50:48 2018

@author: asieb
"""

import math
import pygame
import gamegridp
from gamegridp import image_renderer
from typing import Type


class Actor(pygame.sprite.DirtySprite):

    actor_count = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # private
        self._renderer = image_renderer.ImageRenderer()
        self._image = self._renderer.get_image()
        self._size = (40, 40)  # Tuple with size
        # protected
        self.__flip_x = False
        self.__is_in_grid = False
        self.__is_at_border = False
        self.__is_touching_borders = False
        self.__is_colliding = False
        self.__collision_partners = pygame.sprite.Group()
        self.__colliding_actors = []
        self.__actor_id = Actor.actor_count + 1
        Actor.actor_count += 1
        # public
        self.animation_speed = 60
        self.image_actions = ["flip", "rotate", "scale"]
        self.is_static = False
        self.is_animated = False
        self.direction = 0
        self.grid = None

    def add_image_action(self, value):
        self.image_actions.append(value)

    def add_collision_partner(self, partner):
        self.__collision_partners.add(partner)

    def __str__(self):
        return "Klasse: {0}; ID: {1}".format(self.class_name , self.__actor_id)

    @property
    def image(self):
        if not self.dirty:
            return self._image
        else:
            image = self._renderer.get_image()
            if self.grid.show_info_overlay:
                image = self._renderer.draw_direction_overlay(image, (255, 255, 0), self.direction)
            if "scale" in self.image_actions:
                image = image_renderer.ImageRenderer.scale_image(image, self.size)
            if "center" in self.image_actions:
                image = image_renderer.ImageRenderer.center_image(image, self.size, self.grid.cell_size)
            if "flip" in self.image_actions:
                image = image_renderer.ImageRenderer.flip_image(image, self.__flip_x, False)
            if "rotate" in self.image_actions:
                image = image_renderer.ImageRenderer.rotate_image(image, self.direction)
            return image

    @property
    def rect(self):
        return self.grid.map_rect_to_cell(self.position, self.image.get_rect())

    def add_image(self, img_path: str,):
        return self._renderer.add_image(img_path)

    def _next_sprite(self):
        if self.grid.frame % self.animation_speed == 0:
            self._renderer.next_sprite()

    @property
    def direction(self) -> int:
        """int: Legt die Richtung fest, in die der Akteur "schaut"
            0° bezeichnet dabei nach Osten, andere Winkel werden gegen den Uhrzeigersinn angegeben.
            Die Direction kann alternativ auch als String ("left", "right", "top", "bottom"  festgelegt werden.
        """
        return self._direction

    @direction.setter
    def direction(self, value):
        direction = self._value_to_direction(value)
        self._direction = direction
        self.changed()

    @property
    def size(self):
        """int: Legt die Richtung fest, in die der Akteur "schaut"
            0° bezeichnet dabei nach Osten, andere Winkel werden gegen den Uhrzeigersinn angegeben.
            Die Direction kann alternativ auch als String ("left", "right", "top", "bottom"  festgelegt werden.
        """
        return self._size

    def set_size(self, value):
        self._size = value
        self.changed()

    def animate(self):
        """
        Startet eine Animation.
        """
        if not self.is_animated:
            self.is_animated = True

    @property
    def position(self) -> tuple:
        return self._position

    @position.setter
    def position(self, value: tuple):
        self._position = value
        self.changed()

    @property
    def class_name(self) -> str:
        return self.__class__.__name__

    # Methoden
    def act(self):
        """
        Überschreibe diese Methode in deinen eigenen Actor-Klassen
        """
        pass

    def stop(self):
        """
        Stopt die Animation eines Akteurs.
        """
        self.is_animated = False

    def flip_x(self):
        """
        Spiegelt das Bild des Akteurs über die y-Achse.
        Der Akteur selbst wird dabei um 180° gedreht.
        """
        if not self.__flip_x:
            self.__flip_x = True
        else:
            self.__flip_x = False
        self.turn_left(180)

    def set_bounding_box_size(self, value):
        """
        Legt die Größe der umgebenen Bounding-Box fest.

        :param value: Eine Größe (width, height) als Tupel.
        """
        self.__bounding_box_size = value

    def listen(self, key, data = None):
        """
        Diese Methode sollte in deiner Kind-Klasse überschrieben werden.
        """
        pass

    @property
    def x(self):
        """
        Gibt die x-Koordinate des Akteuers zurück.

        :param x: Gibt die x-Koordinate des Akteurs zurück.
        """
        return self.position[0]

    @x.setter
    def x(self, x):
        """
        Setzt die x-Koordinate der Akteurs.
        :param x: Die x-Koordinate die gesetzt werden soll.
        """
        self.position = (x, self.position[1])

    @property
    def y(self):
        """
        Gibt die y-Koordinate des Akteuers zurück.

        :param y: Gibt die y-Koordinate des Akteurs zurück
        """
        return self.position[1]

    @y.setter
    def y(self, y):
        """
        Setzt die y-Koordinate der Akteurs.

        :param y: Die y-Koordinate die gesetzt werden soll.
        """
        self.position = (self.position[0], y)

    def setup(self):
        """
        Sollte in deiner Kind-Klasse überschrieben werden.
        """
        pass

    def turn_left(self, degrees: int = 90) -> int:
        """
        Dreht den Akteur um degrees Grad nach links.

        :param degrees: Die Gradzahl um die der Akteur gedreht wird.

        :return: Die neue Richtung in Grad.
        """
        print("turn left", self.direction, degrees)
        direction = self.direction + degrees
        self.direction = direction
        print("turn left", self.direction, degrees)
        return self.direction

    def turn_right(self, degrees: int = 90):
        """
        Der Actor dreht sich um 90° nach rechts.

        :param degrees: Richtung in Grad.

        :return: Neue Richtung in Grad.
        """
        direction = self.direction - degrees
        self.direction = direction
        return self.direction

    def move_back(self, distance: int = 1):
        destination = self.look("forward", distance)
        self.position = destination

    def move(self, direction : str = "forward", distance : int = 1):
        self.direction = self._value_to_direction(direction)
        destination = self.look(direction, distance)
        self.position = destination

    def look(self, direction: str = "forward", distance: int = 1) -> tuple:
        direction = self._value_to_direction(direction)
        x = round(self.position[0] + math.cos(math.radians(direction)) * distance)
        y = round(self.position[1] - math.sin(math.radians(direction)) * distance)
        return x, y

    def update(self):
        self._next_sprite()

    def changed(self):
        self.dirty = 1
        self.__update_status()

    def _value_to_direction(self, value) -> int:
        if value == "right":
            value = 0
        if value == "left":
            value = 180
        if value == "up":
            value = 90
        if value == "down":
            value = 270
        if value == "forward":
            value = self.direction
        if value == "back":
            value = 360 - self.direction
        value = value % 360
        return value

    def remove(self):
        """
        Entfernt den Akteur vom Grid.
        """
        self.grid.remove_actor(self)
        del (self)

    def __update_status(self):
        try:
            in_grid = self.is_in_grid()
            if in_grid != self.__is_in_grid:
                self.__is_in_grid = in_grid
                self.grid.get_event("in_grid", self)
            at_border = self.is_at_border()
            if at_border != self.__is_at_border:
                self.__is_at_border = at_border
                self.grid.get_event("at_border", self)
            colliding = self.is_colliding()
            if colliding != self.__is_colliding:
                colliding_actors = self.get_colliding_actors()
                self.__is_colliding = colliding
                self.__collision_partners = None
                for col_partner in colliding_actors:
                    if col_partner not in self.__colliding_actors:
                        col_partner.__colliding_actors.append(self)
                        self.get_event("collision", (self, col_partner))
        except AttributeError:
            pass

    def is_colliding(self):
        return self.grid.is_colliding(self)

    def get_colliding_actors(self):
        return self.grid.get_colliding_actors(self)

    def is_colliding_with(self, class_name):
        colliding_actors = self._grid.get_colliding_actors(self)
        return gamegridp.GameGrid.filter_actor_list(colliding_actors, class_name)

    def is_at_border(self):
        return self.grid.is_at_border(self.rect)

    def is_in_grid(self):
        return self.grid.is_in_grid(self.rect)

    def get_event(self, event, data):
        pass