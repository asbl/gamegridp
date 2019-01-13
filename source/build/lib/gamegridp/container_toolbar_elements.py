import os
from gamegridp import container
import pygame

class ToolbarElement():
    def __init__(self, width, height, background_color):
        package_directory = os.path.dirname(os.path.abspath(__file__))
        self.myfont = pygame.font.SysFont("monospace", 15)
        self.background_color = background_color
        self.event = "no event"
        self._dirty = 1
        self._init_state()
        self.width = width
        self.height = height
        self.parent = None
        self.background_color = background_color

    def _init_state(self):
        self._text = ""
        self._image = None
        self._border = False
        self._text_padding = 5
        self._img_path = None

    def setup(self, parent):
        self.parent = parent
        self.dirty = 1

    def get_surface(self):
        return self.surface

    def call_click_event(self, button, pos_x, pos_y):
        return self.event, 0

    @property
    def dirty(self):
        return self._dirty

    @dirty.setter
    def dirty(self, value):
        self._dirty = value
        if self.parent:
            self.parent.dirty = value

    def clear(self):
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill(self.background_color)
        self.dirty = 1
        return self.surface

    def repaint(self):
        self.clear()
        self.draw_surface()

    def draw_surface(self):
        label = self.myfont.render(self._text, 1, (0, 0, 0))
        self.surface.blit(label, (self._text_padding, 5))
        if self._img_path is not None:
            image = pygame.image.load(self._img_path)
            image = pygame.transform.scale(image, (22, 22))
            self.surface.blit(image, (2, 0))
        if self._border:
            border_rect = pygame.Rect(0, 0, self.width, self.height - 2)
            pygame.draw.rect(self.surface, self.background_color, border_rect, self.width)


    def set_text(self, text):
        self._text = text
        self.dirty = 1

    def set_image(self, img_path):
        self._img_path = img_path
        self.dirty = 1

    def set_border(self, color, width):
        self.border = True
        self.dirty = 1

class ToolbarButton(ToolbarElement):

    def __init__(self, width, height, text, img_path, color=(255,255,255), border=(255,255,255)):
        super().__init__(width, height, color)
        self.surface.fill(color)
        if img_path is not None:
            self.set_image(img_path)
            self.set_text(text, 25)
        else:
            self.set_text(text,2)
        self.event = "button"
        self.data = text

    def call_click_event(self, button, pos_x, pos_y):
        return self.event, self.data


class ToolbarLabel(ToolbarElement):

    def __init__(self, width, height, text, img_path, color=(0,255,255), border=(255,255,255)):
        super().__init__(width, height, color)
        self.set_image(img_path)
        self.set_text(text)
        self.event = "label"
        self.data = text