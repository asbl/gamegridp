from gamegridp import *
import math
import pygame
from collections import defaultdict


class CellGrid(GameGrid):
    """
    Das Cell-Grid ist gedacht für Grids, deren Zellen größer als 1 Pixel sind.
    """
    def __init__(self, cell_size=1, columns=20, rows=16, margin=0):
        super().__init__(cell_size = cell_size, columns= columns, rows = rows, margin = margin)
        self._dynamic_actors_dict = defaultdict(list) # the dict is regularly updated
        self._dynamic_actors = [] # List with all dynamic actors
        self._static_actors_dict = defaultdict(list)


    def _update_actors_positions(self) -> None:
        self._dynamic_actors_dict.clear()
        for actor in self._dynamic_actors:
            x, y = actor.position[0], actor.position[1]
            self._dynamic_actors_dict[(x, y)].append(actor)

    def get_colliding_actors(self, actor: Actor) -> list:
        self._update_actors_positions()
        x, y = actor.position[0], actor.position[1]
        colliding_actors = self.actors_in_area(actor.rect)
        if actor in colliding_actors:
            colliding_actors.remove(actor)
        return colliding_actors

    def actors_in_area(self, area: pygame.Rect) -> list:
        self._dynamic_actors_dict.clear()
        self._update_actors_positions()
        x, y = self.pixel_to_cell(area.topleft)
        self.log.info("x {0},y {1}".format(x,y))
        actors = []
        if self.is_in_grid(self.rect):
            if self._dynamic_actors_dict[x, y]:
                actors.extend(self._dynamic_actors_dict[(x, y)])
            if self._static_actors_dict[x, y]:
                actors.extend(self._static_actors_dict[(x, y)])
        self.log.info("actors:" + str(actors))
        return actors

    def remove_actor(self, actor: Actor)-> None:
        if actor in self._dynamic_actors:
            self._dynamic_actors.remove(actor)
        if actor in  self._static_actors_dict[(actor.x, actor.y)]:
            self._static_actors_dict[(actor.x, actor.y)].remove(actor)
        super().remove_actor(actor)

    def remove_actors_from_cell(self, cell: tuple)->None:
        """
        Entfernt alle Actors aus einer Zelle
        Parameters
        ----------
        cell : Die Zelle aus der der Akteur entfernt werden soll.

        Returns
        -------

        """
        for actor in self._dynamic_actors_dict[cell[0], cell[1]]:
            self.remove_actor(actor)
        for actor in self._static_actors_dict[cell[0], cell[1]]:
            self.remove_actor(actor)

    def add_actor(self, actor: Actor, position : tuple = None) -> Actor:
        if actor.is_static:
            self._static_actors_dict[(position[0], position[1])].append(actor)
        else:
            self._dynamic_actors.append(actor)
        super().add_actor(actor, position)
        if actor.size == (0, 0):
            actor.size = (self.cell_size, self.cell_size)
        return actor

    def update_actor(self, actor : Actor, attribute, value):
        if attribute == "is_static" and value is True:
            self._static_actors_dict[(actor.x(), actor.y())].append(actor)
            if actor in self._dynamic_actors_dict:
                self._dynamic_actors_dict.pop(actor)
        else:
            self._dynamic_actors.append(actor)

    def is_empty_cell(self, cell: tuple) -> bool:
        """
        Überprüfe, ob eine Zelle leer ist.

        :param cell: Die Zellenkoordinaten als Tupel (x,y)
        :return: True, falls Ja, ansonsten False
        """
        if not self.get_all_actors_at_location(cell):
            return True
        else:
            return False

    def get_neighbour_cells(self, cell: tuple) -> list:
        """
        Gibt alle 8 umgebenen Zellen zurück.

        :return: Alle Nachbarzellen als Liste.
        """
        cells = []
        y_pos = cell[0]
        x_pos = cell[1]
        cells.append([x_pos + 1, y_pos])
        cells.append([x_pos + 1, y_pos + 1])
        cells.append([x_pos, y_pos + 1])
        cells.append([x_pos - 1, y_pos + 1])
        cells.append([x_pos - 1, y_pos])
        cells.append([x_pos - 1, y_pos - 1])
        cells.append([x_pos, y_pos - 1])
        cells.append([x_pos + 1, y_pos - 1])
        return cells

    def is_in_grid(self, rect: pygame.Rect) -> bool:
        x, y = self.pixel_to_cell(rect.center)
        if x > self.columns - 1:
            return False
        elif y > self.rows - 1:
            return False
        elif x < 0 or y < 0:
            return False
        else:
            return True

    def is_at_border(self, actor : Actor) -> str:
        if actor.x == self.columns - 1:
            return "right"
        elif actor.y == self.rows - 1:
            return "bottom"
        elif actor.x == 0:
            return "left"
        elif actor.y == 0:
            return "top"
        else:
            return None
