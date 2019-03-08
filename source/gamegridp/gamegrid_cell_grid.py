from gamegridp import gamegrid
import math
import pygame
from collections import defaultdict


class CellGrid(gamegrid.GameGrid):
    """
    Das Cell-Grid ist gedacht für Grids, deren Zellen größer als 1 Pixel sind.
    """
    def __init__(self, cell_size=1, columns=40, rows=40, margin=0):
        super().__init__(cell_size = cell_size, columns= columns, rows = rows, margin = margin)
        self._dynamic_actors_dict = defaultdict(list)
        self._static_actors_dict = defaultdict(list)
        self._dynamic_actors = []

    def update_actor_positions(self):
        # update the dynamic_collison dict before calling the collisions
        self._dynamic_actors_dict.clear()
        for actor in self._dynamic_actors:
            x, y = actor.position[0], actor.position[1]
            self._dynamic_actors_dict[(x, y)].append(actor)

    def get_colliding_actors(self, actor) -> list:
        self.update_actor_positions()
        x, y = actor.position[0], actor.position[1]
        colliding_actors = self.get_all_actors_at_position((x, y))
        if actor in colliding_actors:
            colliding_actors.remove(actor)
        return colliding_actors

    def get_all_actors_at_position(self, position):
        self.update_actor_positions()
        x, y = position[0], position[1]
        actors = []
        if self.is_in_grid((x, y)):
            if self._dynamic_actors_dict[x, y]:
                actors.extend(self._dynamic_actors_dict[(x, y)])
            if self._static_actors_dict[x, y]:
                actors.extend(self._static_actors_dict[(x, y)])
        return actors

    def remove_actor(self, actor):
        if actor in self._dynamic_actors:
            self._dynamic_actors.remove(actor)
        if actor in  self._static_actors_dict[(actor.x, actor.y)]:
            self._static_actors_dict[(actor.x, actor.y)].remove(actor)
        super().remove_actor(actor)

    def remove_actors_from_cell(self, location):
        """
        Entfernt alle Actors aus einer Zelle
        Parameters
        ----------
        location : Die Zelle aus der der Akteur entfernt werden soll.

        Returns
        -------

        """
        for actor in self._dynamic_actors_dict[location[0], location[1]]:
            self.remove_actor(actor)
        for actor in self._static_actors_dict[location[0], location[1]]:
            self.remove_actor(actor)

    def add_actor(self, actor, position=None):
        if actor.is_static:
            self._static_actors_dict[(actor.get_x(), actor.get_y())].append(actor)
        else:
            self._dynamic_actors.append(actor)
        super().add_actor(actor, position)

    def update_actor(self, actor, attribute, value):
        if attribute == "is_static" and value is True:
            self._static_actors_dict[(actor.get_x(), actor.get_y())].append(actor)
            if actor in self._dynamic_actors_dict:
                self._dynamic_actors_dict.remove(actor)
        else:
            self._dynamic_actors.append(actor)
        super()._update_actor(actor, attribute, value)


    def add_cell_image(self, img_path: str, location: tuple):
        """
        Fügt ein Bild zu einer einzelnen Zelle hinzu

        :param img_path: Der Pfad zum Bild relativ zum aktuellen Verzeichnis
        :param location: Die Zelle, die "angemalt" werden soll.
        """
        top_left = self.cell_to_pixel(location)
        cell_image = pygame.image.load(img_path).convert()
        cell_image = pygame.transform.scale(cell_image, (self.cell_size, self.cell_size))
        self._image.blit(cell_image, (top_left[0], top_left[1], self.cell_size, self.cell_size))

    @property
    def type(self):
        return "cell"

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

    def get_neighbour_cells(self, cell) -> list:
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

    def is_in_grid(self, position):
        x, y = position[0], position[1]
        if x > self.columns - 1:
            return False
        elif y > self.rows - 1:
            return False
        elif x < 0 or y < 0:
            return False
        else:
            return True

    def is_at_border(self, actor):
        if actor.x == self.columns - 1:
            return "right"
        elif actor.y == self.rows - 1:
            return "bottom"
        elif actor.x == 0:
            return "left"
        elif actor.y == 0:
            return "top"
        else:
            return False