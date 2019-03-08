# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 21:49:29 2018

@author: Andreas Siebel
"""
import pygame
import window as gamegrid_window
import container as container
import image_renderer


class GameGrid(container.Container):

    def __init__(self, cell_size=1, columns=40, rows=40, margin=0):
        super().__init__(self)
        pygame.init()
        # public
        self.is_running = False
        self.speed = 60
        self.active_actor = None
        self.image_action = None
        self.is_static = False
        # private
        self._renderer = image_renderer.ImageRenderer()
        self._show_info_overlay = False
        self._actors = pygame.sprite.LayeredDirty()
        self._key_pressed = False
        self._key = 0
        self._animated = False
        self._grid = []
        self.cell_size = cell_size
        self._columns, self._rows = columns, rows
        print("c,r in init:", self.columns, self.rows)
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
        self._surface = pygame.Surface((self.width, self.height))
        self.dirty = 1
        self._window = gamegrid_window.GameGridWindow("Gamegrid")
        self._window.add_container(self, "main")

    def set_size(self,cell_size=1, columns=40, rows=40, margin=0):
        self.cell_size = cell_size
        self._columns = columns
        self._rows = rows
        self._cell_margin = margin
        self._grid = []
        print("c,r:", self.columns, self.rows)
        for row in range(self.rows):
            self._grid.append([])
            for column in range(self.columns):
                self._grid[row].append(0)
        self.dirty = 1

    @staticmethod
    def filter_actor_list(list, class_name):
        return [actor for actor in list if actor.__class__.__name__ == class_name]

    def get_event(self, event, data = None):
        pass

    def is_colliding(self, actor) -> bool:
        colliding_actors = self.get_colliding_actors(actor)
        if colliding_actors:
            return True
        else:
            return False

    @property
    def width(self):
        if self.dirty == 0:
            return self._container_width
        else:
            self._container_width = self.columns * self._cell_size + (self.columns + 1) * self._cell_margin
            return self._container_width

    @property
    def height(self):
        if self.dirty == 0:
            return self._height
        else:
            self._height = self.rows * self._cell_size + (self.columns + 1) * self._cell_margin
            return self._height



    @property
    def window(self):
        """die Größe der einzelne Zellen des Grids."""
        return self._window

    @property
    def cell_size(self):
        """die Größe der einzelne Zellen des Grids."""
        return self._cell_size

    @property
    def cell_margin(self):
        """
        returns the margin between cells
        """
        return self._cell_margin

    @cell_size.setter
    def cell_size(self, value: int):
        """ Sets the cell-size"""
        self._cell_size = value

    @property
    def rows(self):
        """
        returns the margin between cells
        """
        return self._rows

    @property
    def columns(self):
        """
        returns the margin between cells
        """
        return self._columns

    @property
    def actors(self):
        """
        returns all actors in grid
        :return: a list of all actors
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
        return self.__class__.__name__

    def add_image(self, img_path: str):
        self._image = self._renderer.add_image(img_path)

    @property
    def image(self):
        if not self.dirty:
            return self._image
        else:
            image = self._renderer.get_image()
            image = self._renderer.scale_image(image, (self.width, self.height))
            return image

    def add_actor(self, actor, position):
        """
        Fügt einen Actor zum Grid hinzu

        Parameters
        ----------
        actor : gamegridp.Actor
            Der Actor, der hinzugefügt werden soll
        cell :
            Der Ort, an dem der Actor hinzugefügt werden soll.

        """
        self.actors.add(actor)
        actor.position = position
        actor.grid = self
        actor.dirty = 1

    def get_actors_by_pixel(self, coordinates):
        actors = []
        for actor in self.actors:
            if actor.rect.collidepoint(coordinates):
                actors.append(actor)
        return actors

    def _call_collision_events(self):
        pass

    def all_collisions(self, actor):
        pass

    def test_collision(self, actor1, actor2) -> bool:
        pass

    def remove_actor(self, actor):
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
        self.setup()
        self.dirty = 1

    def stop(self):
        """
        Stoppt die Ausführung (siehe auch run)
        """
        self.__running = False

    def run(self):
        """
        Startet die Ausführung (equivalent zum Drücken des Run-Buttons).
        Wenn das Spiel läuft handeln die Akteure mit jedem Durchlauf der mainloop genau einmal.
        """
        self.__running = True

    def _pixel_to_cell(self, pos: tuple):
        """
        transforms a pixel-coordinate into a cell coordinate in grid
        :param pos: the position in pixels
        """
        column = \
            (pos[0] - self._cell_margin) // (self._cell_size + self._cell_margin)
        row = \
            (pos[1] - self._cell_margin) // (self._cell_size + self._cell_margin)
        return column, row

    def cell_to_rect(self, cell: tuple):
        """
        Gibt das Rechteck zurück, dass eine Zelle umschließt.
        """
        x = cell[0] * self._cell_size + cell[0] * self._cell_margin + self._cell_margin
        y = cell[1] * self._cell_size + cell[1] * self._cell_margin + self._cell_margin
        return pygame.Rect(x, y, self._cell_size, self._cell_size)

    def cell_to_pixel(self, cell: tuple):
        """
        Gibt die obere-linke Koordinate einer Zelle zurück.
        """
        x = cell[0] * self._cell_size + cell[0] * self._cell_margin + self._cell_margin
        y = cell[1] * self._cell_size + cell[1] * self._cell_margin + self._cell_margin
        return pygame.Rect(x, y, self._cell_size, self._cell_size)

    def map_rect_to_cell(self, cell, rect):
        column, row = cell[0], cell[1]
        overlapping_x, overlapping_y = 0, 0
        cell_margin, cell_size = self.cell_margin, self.cell_size
        width = rect.width
        height = rect.height
        if width > cell_size:
            overlapping_x = (width - cell_size) / 2
        if height > cell_size:
            overlapping_y = (height - cell_size) / 2
        left = cell_margin + (cell_margin + cell_size) * column - overlapping_x
        top = cell_margin + (cell_margin + cell_size) * row - overlapping_y
        return pygame.Rect(left, top, width, height)

    @property
    def show_info_overlay(self):
        return self._show_info_overlay

    @show_info_overlay.setter
    def show_info_overlay(self, value: bool):
        if value is True:
            self._show_info_overlay = True
            self.dirty = 1
        else:
            self._show_info_overlay = False
            self.dirty = 1

    def is_in_grid(self, rect) -> bool:
        if rect.topleft[0] < 0:
            return False
        if rect.topleft[1] < 0:
            return False
        if rect.topleft[0] + rect.width > self.width:
            return False
        if rect.topleft[1] + rect.height > self.height:
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
        self._window.repaint_areas.extend(self.actors.draw(self._surface))
        if self.dirty == 1:
            self._window.repaint_areas.append(self.rect())
            self.dirty = 0

    def show(self):
        """
        Startet das Programm.
        """
        self.actors.clear(self._surface, self.image)
        print(self.columns, self.rows)
        self._surface = pygame.Surface((self.width, self.height))
        self.dirty = 1
        self.window.show()

    def update(self):
        if self.__running:
            self.__act_all()
        self.__frame = self.__frame + 1
        for actor in self.actors:
            actor.update()
        if self.__frame == 100:
            self.__frame = 0
        self.__clock.tick(60)

    def __act_all(self):
        self.__tick = self.__tick + 1
        if self.__tick > 60 - self.speed:
            for actor in self.actors:
                actor.act()
            self.act()
            self.__tick = 0

    def pass_event(self, event, data = None):
        for actor in self.actors:
            actor.get_event(event, data)

    def act(self):
        """
        Überschreibe diese Methode in deinen Kind-Klassen
        """
        pass