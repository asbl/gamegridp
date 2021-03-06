import pygame
from gamegridp.containers import *
from gamegridp.actors import *
from gamegridp.window import *
import logging
from typing import Union
import sys


class GameGrid(Container):

    log = logging.getLogger("GameGrid")

    def __init__(self,
                 cell_size: int = 1,
                 columns: int = 40,
                 rows: int = 40,
                 margin: int =0):
        """
        initializes a new GameGrid
        :param cell_size: The cell_size in pixels
        :param columns: The number of columns
        :param rows: The number of rows
        :param margin: the margin between cells
        """
        super().__init__(self)
        pygame.init()
        # public
        self.is_running = False
        self.speed = 60
        self.active_actor = None
        self.is_static = False
        # private
        self._renderer = ImageRenderer()
        self.set_image_action("info_overlay", False)
        self._show_info_overlay = False
        self._actors = pygame.sprite.LayeredDirty()
        self._key_pressed = False
        self._key = 0
        self._animated = False
        self._grid = []
        self._cell_size = cell_size
        self._columns, self._rows = columns, rows
        self._cell_margin = margin
        self.set_size(cell_size, columns, rows, margin)
        # protected
        self.dirty = 1
        self.__frame = 0
        self.__tick = 0
        self.__clock = pygame.time.Clock()
        self.__last_update = pygame.time.get_ticks()
        self.__running = True
        # Init graphics
        self._image = pygame.Surface((0, 0))
        self.dirty = 1
        self._window = GameGridWindow("Gamegrid")
        self._window.add_container(self, "main")

    def set_size(self,
                 cell_size: int = 1,
                 columns: int = 40,
                 rows: int = 40,
                 margin: int = 0):
        """
        Sets size of a gamegrid
        :param cell_size: The cell_size in pixels
        :param columns: The number of columns
        :param rows: The number of rows
        :param margin: the margin between cells
        """
        self.cell_size = cell_size
        self._columns = columns
        self._rows = rows
        self._cell_margin = margin
        self._grid = []
        self.log.info("Set GameGrid Size to {0} columns and {1} rows".format(self.columns, self.rows))
        for row in range(self.rows):
            self._grid.append([])
            for column in range(self.columns):
                self._grid[row].append(0)
        self.dirty = 1

    def __str__(self):
        return "[Grid with {0} columns and {1} rows]".format(self.columns, self.rows)

    @staticmethod
    def filter_actor_list(a_list, actor_type):
        return [actor for actor in a_list if type(actor) == actor_type]

    def get_event(self, event, data):
        """
        Returns events triggered by events.
        :param event: The event
        :param data: The data of the event
        """
        pass

    def is_colliding(self, actor) -> bool:
        colliding_actors = self.get_colliding_actors(actor)
        if colliding_actors:
            return True
        else:
            return False

    @property
    def width(self) -> int:
        """
        :return: Returns the width of the boards
        """
        if self.dirty == 0:
            return self._container_width
        else:
            self._container_width = self.columns * self._cell_size + (self.columns + 1) * self._cell_margin
            return self._container_width

    @property
    def height(self) -> int:
        """
        :return: Returns the height of the boards
        """
        if self.dirty == 0:
            return self._container_height
        else:
            self._container_height = self.rows * self._cell_size + (self.rows + 1) * self._cell_margin
            return self._container_height

    @property
    def window(self) -> GameGridWindow:
        """
        :return: returns the parent window
        """
        return self._window

    @property
    def cell_size(self):
        """
        :return: The Cell_size in pixels
        """
        return self._cell_size

    @cell_size.setter
    def cell_size(self, value: int):
        """ Sets the cell-size"""
        self._cell_size = value

    @property
    def cell_margin(self) -> int:
        """
        :return: The margin between cells
        """
        return self._cell_margin

    @property
    def rows(self) -> int:
        """
        :return: number of rows of the boards
        """
        return self._rows

    @property
    def columns(self) -> int:
        """
        :return: number of columns of the boards
        """
        return self._columns

    @property
    def actors(self) -> list:
        """
        :return: A list of all actors
        """
        return self._actors

    @property
    def frame(self) -> int:
        """
        Returns the actual frame
        :return: the value of actual frame
        """
        return self.__frame

    @property
    def class_name(self) -> str:
        """
        :return: The Class Name of Actor
        """
        return self.__class__.__name__

    def set_image_action(self, attribute : str, value : bool):
            self._renderer.image_actions[attribute] = value

    def add_image(self, img_path: str) -> pygame.Surface:
        """
        :param img_path: The path to the image
        :return: The image
        """
        return self._renderer.add_image(img_path)

    @property
    def image(self):
        if not self.dirty:
            return self._image
        else:
            self._renderer.size = (self._container_width, self._container_height)
            self._renderer.cell_size = self.cell_size
            self._renderer.margin = self.cell_margin
            _image = self._renderer.get_image()
            self._image = _image
            return _image

    def add_actor(self, actor: Actor, position : tuple) -> Actor:
        """
        adds actors to boards
        :param actor: the actors as subclass of Actor
        :param position: the position in the boards
        :return: The Actor
        """
        try:
            self.actors.add(actor)
            actor.position = position
            actor.grid = self
            actor.dirty = 1
            if actor.init != 1:
                raise UnboundLocalError("Init was not called")
            self.log.info("Added actors {0} to {1} at position {2} with rect {3}".format(actor, self, actor.position, actor.rect))
            return actor
        except UnboundLocalError as e:
            self.log.error("super().__init__() of actors: {0} was not called".format(actor))
            raise

    def get_actors_by_pixel(self, pixel : tuple) -> list:
        """
        Returns all players who have a certain pixel in common
        :param pixel: The pixel-coordinates
        :return: All actors as list
        """
        actors = []
        for actor in self.actors:
            if actor.rect.collidepoint(pixel):
                actors.append(actor)
        return actors

    def _call_collision_events(self):
        pass

    def get_actors_at_location(self, value: Union[pygame.Rect, tuple]) -> list:
        """
        Gets all actors at location
        :param value: Either a tuple with cell cordinates a Rect
        :return:
        """
        actors = []
        if type(value) == tuple:
            value = pygame.Rect(value[0],value[1],1,1)
        for actor in actors:
            if actor.rect.colliderect(value):
                actors.append(actor)
        return actors

    def remove_actors_from_location(self, location: Union[tuple, pygame.Rect], actor_type = None):
        """
        Removes actors from an area or position
        :param location: The location can be either a Rect or a tuple with cell_coordinates
        :param actor_type: Filters actors by type (e.g. all <Player>-Objects at position)
        """
        actors = []
        if type(location) == tuple:
            location = pygame.Rect(location[0], location[1], 1, 1)
        actors = self.get_actors_at_location(location)
        if actor_type is not None:
            actors = self.filter_actor_list(actors, actor_type)
        for actor in actors:
            self.remove_actor(actor)

    def remove_actor(self, actor : Actor):
        if actor:
            self.actors.remove(actor)
            actor.grid = None

    def remove_all_actors(self):
        """
        Entfernt alle Akteure aus dem Grid.
        """
        for actor in self.actors:
            self.remove_actor(actor)

    def reset(self):
        self.dirty = 1

    def stop(self):
        """
        Stoppt die Ausführung (siehe auch run)
        """
        self.__running = False

    def run(self):
        self.__running = True

    def is_in_grid(self, value: Union[tuple, pygame.Rect]) -> bool:
        if type(value) == tuple:
            value = self.cell_to_rect(value)
        top_left_x, top_left_y, right, top = value.topleft[0], \
                                         value.topleft[1], \
                                         value.right, \
                                         value.top
        if top_left_x < 0 or top_left_y < 0 or  right > self.width or top > self.height:
            return False
        else:
            return True

    def get_touching_borders(self, actor) -> list:
        return []

    def is_at_border(self, actor):
        borders = self.get_touching_borders(actor)
        if borders:
            return True
        else:
            return False

    def get_colliding_actors(self, actor) -> list:
        pass

    def repaint(self):
        self._window.repaint_areas.extend(self.actors.draw(self.image))
        if self.dirty == 1:
            self._window.repaint_areas.append(self.rect)
            self.dirty = 0

    def show(self):
        """
        Starts the program
        """
        self.actors.clear(self.image, self.image)
        self.dirty = 1
        logging.basicConfig(level=logging.WARNING)
        self.window.show()

    def update(self):
        if self.__running:
            self._act_all()
        self.__frame = self.__frame + 1
        for actor in self.actors:
            actor.update()
        self._call_collision_events()
        if self.__frame == 100:
            self.__frame = 0
        self.__clock.tick(60)

    def _act_all(self):
        self.__tick = self.__tick + 1
        if self.__tick > 60 - self.speed:
            for actor in self.actors:
                actor.act()
            self.act()
            self.__tick = 0

    def pass_event(self, event, data = None):
        if event != "collision":
            for actor in self.actors:
                actor.get_event(event, data)
        if event == "collision":
            for actor in self.actors:
                if data[0] == actor:
                    actor.get_event("collision", data[1])
                elif data[1] == actor:
                    actor.get_event("collision", data[0])

    def act(self):
        """
        Überschreibe diese Methode in deinen Kind-Klassen
        """
        pass

    def rect_to_position(self, position : tuple, rect : pygame.Rect) -> pygame.Rect:
        """
        Centers a rectangle over a cell
        :param position: (x, y): Position of rectangle
        :param rect: the rectangle
        :return: centered rectangle
        """
        top_left = self.cell_top_left((position[0], position[1]))
        new_rect = pygame.Rect(0, 0,rect.width,rect.height)
        new_rect.topleft = top_left
        return new_rect

    def pixel_to_cell(self, position: tuple) -> tuple:
        """
        Returns the cell in which the pixel coordinates are located.
        :param position: (x, y), pixel coordinates
        :return: (x,y) a gamegrid cell
        """
        column = (position[0] - self._cell_margin) // (self._cell_size + self._cell_margin)
        row = (position[1] - self._cell_margin) // (self._cell_size + self._cell_margin)
        return column, row

    def cell_to_rect(self, cell: tuple) -> pygame.Rect:
        """
        Returns the enclosing rectangle.
        :param cell: (x, y), cell coordinates
        :return: the enclosing rectangle
        """
        x = cell[0] * self._cell_size + cell[0] * self._cell_margin + self._cell_margin
        y = cell[1] * self._cell_size + cell[1] * self._cell_margin + self._cell_margin
        return pygame.Rect(x, y, self._cell_size, self._cell_size)

    def cell_top_left(self,cell: tuple) -> tuple:
        rect = self.cell_to_rect(cell)
        return rect.topleft

    def show_log(self):
        logging.basicConfig(level=logging.INFO)