# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 21:50:48 2018

@author: asieb
"""

import logging
import math
import pygame
from gamegridp import image_renderer


class Actor(pygame.sprite.DirtySprite):

    actor_count = 0

    def __init__(self, grid, position: tuple, **kwargs):
        super().__init__(kwargs)
        # private
        self._grid = grid
        self._renderer = image_renderer.ImageRenderer()
        self._image = self._renderer.get_image()
        #protected
        # protected
        self._flip_x = False
        self.__is_in_grid = False
        self.__is_at_border = False
        self.__is_touching_borders = False
        self.__is_colliding = False
        self.__collision_partners = pygame.sprite.Group()
        self.__colliding_actors = []
        # public
        self.animation_speed = 60
        self.image_actions = ["flip", "rotate"]
        self.is_static = False
        self.is_animated = False
        self._size = (40, 40)  # Tuple with size
        self._position = position
        self.direction = 0
        self.__actor_id = Actor.actor_count + 1
        Actor.actor_count += 1
        self._grid.add_actor(self, position)
        self.setup()
        self.changed()

    def add_collision_partner(self, partner):
        self.__collision_partners.add(partner)

    def __str__(self):
        return self.class_name +",id:" + str(self.__actor_id) + super().__str__()

    @property
    def image(self):
        if not self.dirty:
            return self._image
        else:
            image = self._renderer.get_image()
            if self._grid.show_info_overlay:
                image = self._renderer.draw_direction_overlay(image, (255, 255, 0), self.direction)
            if "scale" in self.image_actions:
                image = image_renderer.ImageRenderer.scale_image(image, self.size)
            if "center" in self.image_actions:
                image = image_renderer.ImageRenderer.center_image(image, self.size, self._grid.cell_size)
            if "flip" in self.image_actions:
                image = image_renderer.ImageRenderer.flip_image(image, self._flip_x, False)
            if "rotate" in self.image_actions:
                image = image_renderer.ImageRenderer.rotate_image(image, self.direction)
            return image

    @property
    def rect(self):
        return self.grid.map_rect_to_cell(self.position, self.image.get_rect())

    def add_image(self, img_path: str,):
        return self._renderer.add_image(img_path)

    def _next_sprite(self):
        if self._grid.frame % self.animation_speed == 0:
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

    @size.setter
    def size(self, value):
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
        if not self._flip_x:
            self._flip_x = True
        else:
            self._flip_x = False
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

    def turn_left(self, degrees: int = 90):
        """
        Dreht den Akteur um degrees Grad nach links.

        :param degrees: Die Gradzahl um die der Akteur gedreht wird.

        :return: Die neue Richtung in Grad.
        """
        direction = self.direction + degrees
        self.direction = direction
        return self.direction

    def turn_right(self, degrees: int = 90):
        """
        Dreht den Akteur um degrees Grad nach links.

        :param degrees: Die Gradzahl um die der Akteur gedreht wird.

        :return: Die neue Richtung in Grad.
        """
        direction = self.direction - degrees
        self.direction = direction
        return self.direction


    def move_back(self, distance: int = 1):
        destination = self.look_back(distance)
        self.position = destination

    def move(self, distance=1, direction = "forward"):
        self.direction = self._value_to_direction(direction)
        destination = self.look_forward(distance)
        self.position = destination

    def look(self, distance: int = 1, direction="forward"):
        direction = self._value_to_direction(direction)
        x = round(self.position[0] + math.cos(math.radians(direction)) * distance)
        y = round(self.position[1] - math.sin(math.radians(direction)) * distance)
        return x, y

    def look_forward(self, distance: int = 1) -> tuple:
        return self.look(distance, "forward")

    def look_back(self, distance: int = 1) -> tuple:
        return  self.look(distance, "back")

    def look_up(self, distance: int = 1) -> tuple:
        return  self.look(distance, "up")

    def look_down(self, distance: int = 1) -> tuple:
        return  self.look(distance, "down")

    def get_all_actors_in_my_cell(self, class_name : str) -> list:
        """
        Gets the first Actor in my cell

        Parameters
        ----------
        class_name Filter actors by class_name

        Returns
        -------
        Returns the found actor or None.
        """
        actors = self.grid.get_all_actors_in_cell(self.position, class_name)
        if self in actors:
            actors.remove(self)
        return actors

    def get_one_actor_in_my_cell(self, class_name : str) -> list:
        """
        Gets the first Actor in my cell
        Parameters
        ----------
        class_name Filter actors by class name

        Returns
        -------
        Returns the found actor or None.
        """
        actor_in_cell = self.grid.get_actor_in_cell(self.position, class_name)
        return actor_in_cell

    def get_actor_in_front(self, class_name, distance = 1) -> list:
        """
        Gets all Actors in front
        Parameters
        ----------
        class_name Filter actors by class name
        distance The distance of fields to look forward

        Returns
        -------
        Returns the found actor or None.
        """
        actor_in_front = self.grid.get_actor_in_cell(self.look_forward(distance), class_name)
        return actor_in_front

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

    @property
    def grid(self):
        return self._grid

    def __update_status(self):
        in_grid = self.is_in_grid()
        if in_grid != self.__is_in_grid:
            self.__is_in_grid = in_grid
            self._grid.get_event("in_grid", self)
        at_border = self.is_at_border()
        if at_border != self.__is_at_border:
            self.__is_at_border = at_border
            self._grid.get_event("at_border", self)
        colliding = self.is_colliding()
        if colliding != self.__is_colliding:
            colliding_actors = self.get_colliding_actors()
            print(colliding_actors)
            self.__is_colliding = colliding
            self.__collision_partners = None
            for col_partner in colliding_actors:
                if col_partner not in self.__colliding_actors:
                    col_partner.__colliding_actors.append(self)
                    self.get_event("collision", (self, col_partner))

    def is_colliding(self):
        return self.grid.is_colliding(self)

    def get_colliding_actors(self, class_name):
        return self._grid.get_colliding_actors(self)

    def is_at_border(self):
        return self.grid.is_at_border(self)

    def is_in_grid(self):
        return self.grid.is_in_grid(self.position)

    def get_event(self, event, data):
        pass