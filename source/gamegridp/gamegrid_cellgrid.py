from gamegridp import gamegrid
import math
import pygame
from collections import defaultdict


class CellGrid(gamegrid.GameGrid):
    """
    Das Cell-Grid ist gedacht für Grids, deren Zellen größer als 1 Pixel sind.
    """
    def __init__(self, title, **kwargs):
        self._dynamic_collision_actors = defaultdict(list)
        self._static_collision_actors = defaultdict(list)
        self._dynamic_actors = []
        super().__init__(title, **kwargs)

    def _call_collisions(self):
        # update the dynamic_collison dict before calling the collisions
        self._dynamic_collision_actors.clear()
        for actor in self._dynamic_actors:
            self._dynamic_collision_actors[(actor.get_x(), actor.get_y())].append(actor)
        super()._call_collisions()

    def get_all_collisions_for_actor(self, actor):
        """
        Gibt einen Actor zurück, dessen Bounding-Boxes mit dem angegebenen Akteur
        kollidieren.

        Parameters
        ----------
        actor Ein Actor vom angegebenen Klassennahmen, der mit dem angegebenen Actor kollidiert.
        class_name Den Klassennamen nach dem gefiltert werden soll.

        Returns
        -------

        """
        collision_actors = self.get_all_actors_in_cell(actor.cell)
        if actor in collision_actors:
            collision_actors.remove(actor)
        return collision_actors

    def get_all_actors_in_cell(self, cell: tuple, class_name: str = "") -> list:
        """
        Gebe alle Akteure an den angegebenen Zellenkoordinaten zurück

        :param cell: Die Zellenkordinaten als Tupel (x,y)
        :param class_name: Den Klassennamen, nachdem gefiltert werden soll
        :return: Eine Liste aller Akteure (mit der angegebenen Klasse) an der Position.
        """
        actors_in_cell = []
        try:
            if self._dynamic_collision_actors[cell[0], cell[1]]:
                actors_in_cell.extend(self._dynamic_collision_actors[(cell[0], cell[1])])
            if self._static_collision_actors[cell[0], cell[1]]:
                actors_in_cell.extend(self._static_collision_actors[(cell[0], cell[1])])
        except:
            pass
        if class_name is not "":
            # Filter list by class_name
            actors_in_cell = [actor for actor in actors_in_cell if actor.__class__.__name__ == class_name]
        return actors_in_cell

    def remove_actor(self, actor):
        if actor in self._dynamic_actors:
            self._dynamic_actors.remove(actor)
        if actor in  self._static_collision_actors[(actor.get_x(), actor.get_y())]:
            self._static_collision_actors[(actor.get_x(), actor.get_y())].remove(actor)
        self._logging.info("Removed"+str(actor))
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
        for actor in self._dynamic_collision_actors[location[0], location[1]]:
            self.remove_actor(actor)
        for actor in self._static_collision_actors[location[0], location[1]]:
            self.remove_actor(actor)

    def add_actor(self, actor, position=None):
        if actor.is_static:
            self._static_collision_actors[(actor.get_x(), actor.get_y())].append(actor)
        else:
            self._dynamic_actors.append(actor)
        super().add_actor(actor, position)

    def update_actor(self, actor, attribute, value):
        if attribute == "is_static" and value is True:
            self._static_collision_actors[(actor.get_x(), actor.get_y())].append(actor)
            if actor in self._dynamic_collision_actors:
                self._dynamic_collision_actors.remove(actor)
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
        if x > self._grid_columns - 1:
            return False
        elif y > self._grid_rows - 1:
            return False
        elif x < 0 or y < 0:
            return False
        else:
            return True

    def is_at_border(self, actor):
        if actor.x == self._grid_columns - 1:
            return "right"
        elif actor.y == self._grid_rows - 1:
            return "bottom"
        elif actor.x == 0:
            return "left"
        elif actor.y == 0:
            return "top"
        else:
            return False