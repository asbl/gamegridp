from gamegridp import gamegrid
from gamegridp import gamegrid_mastergrid
import pygame

class Clock:
    def __init__(self, grid):
        self._grid = grid
        self._start = grid.counter
