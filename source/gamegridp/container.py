import os
import pygame


class Container(object):

    def __init__(self, size: tuple = 0, position="right"):
        self.dirty = 1
        self.background_color = (255,255,255)
        self.size = size
        self.position = position
        # Not mutable
        self._window = None  # Set in add_to_window
        self._width = 0  # Set in add_to_window
        self._height = 0  # Set in add_to_window
        self._window_top_left_x = 0  # Set in add_to_window
        self._window_top_left_y = 0  # Set in add_to_window
        self._window_docking_position = None  # Set in add_to_window
        self._surface = None

    def add_to_window(self, window, window_docking_position):
        self._window = window
        if window_docking_position == "top_left":
            self._window_top_left_x = 0
            self._window_top_left_y = 0
            self._window_docking_position = window_docking_position
            self._height = self._window.y_res
            self._width = self.size
        elif window_docking_position == "right":
            self._window_top_left_x = self._window.x_res
            self._window_top_left_y = 0
            self._window_docking_position = window_docking_position
            self._height = self._window.y_res
            self._width = self.size
        elif window_docking_position == "bottom":
            self._window_top_left_x = 0
            self._window_top_left_y = self._window.y_res
            self._window_docking_position = window_docking_position
            self._width = self._window.x_res
            self._height = self.size
        self._surface = pygame.Surface((self.width, self.height))

    def repaint(self):
        self.blit_surface_to_window_suface()
        if self.dirty == 1:
            self.dirty = 0

    def blit_surface_to_window_suface(self):
        self._window.window_surface.blit(self._surface, self.rect())

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def remove(self):
        pass

    def pass_event(self, event, data):
        pass

    def get_event(self, event, data):
        pass

    def rect(self):
        return pygame.Rect(self._window_top_left_x, self._window_top_left_y, self.width, self.height)

    @property
    def window_docking_position(self):
        return self._window_docking_position

    def updatE(self):
        pass