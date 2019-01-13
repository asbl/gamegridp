import os
import pygame
from gamegridp import container


class Console(container.Container):
    def __init__(self, lines=5, **kwargs):
        super().__init__(**kwargs)
        self._lines = lines
        self._height = self._lines * 20
        self._text_queue = []
        self._dirty = 1

    def _draw_surface(self, surface):
            package_directory = os.path.dirname(os.path.abspath(__file__))
            myfont = pygame.font.SysFont("monospace", 15)
            for i, text in enumerate(self._text_queue):
                line = pygame.Surface((self.width, 20))
                line.fill((200, 200, 200))
                label = myfont.render(text, 1, (0, 0, 0))
                line.blit(label, (0, 0))
                surface.blit(line, (0, i * 20))

    def print(self, text):
        self._text_queue.append(text)
        print(self._text_queue)
        if len(self._text_queue) > self._lines:
            self._text_queue.pop(0)
        self.dirty = 1

    def call_click_event(self, button, pos_x, pos_y):
        pass

