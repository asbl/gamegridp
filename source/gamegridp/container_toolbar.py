import os
import gamegridp
import pygame


class Toolbar(gamegridp.Container):

    def __init__(self, size=100):
        super().__init__(size)
        self._width = size
        self.elements = []
        self.dirty = 1
        self.position = "right"

    def get_element(self, index):
        return self.elements[index]

    def _draw_surface(self, surface):
        """
        Creates a toolbar on the left side of the window
        """
        _actual_height = 0
        for element in self.elements:
            if element.dirty == 1:
                element.repaint()
                surface.blit(element.surface, (0, _actual_height))
                element.dirty = 0
            _actual_height = _actual_height + element.height

    def add_button(self, text, img_path=None, color=(255,255,255), border=(255,255,255)):
        """
          Fügt einen Button zur Toolbar hinzu.
          Parameters
          ----------
          text
              Der Text
          img_path
              Pfad zum Bild vor dem Text (optional)
          color
              Die Hintergrundfarbe
          border
              Die Rahmenfarbe
          Returns
              Der erstellte Button
          """
        button = gamegridp.ToolbarButton(self.width, 25, img_path=img_path, text=text, color=color, border=border)
        button.setup(self)
        self.elements.append(button)
        self.dirty = 1
        return button

    def add_label(self, text, img_path=None, color=(255,255,255), border=(255,255,255)):
        """
        Fügt ein Label zur Toolbar hinzu
        Parameters
        ----------
        text
            Der Text
        img_path
            Pfad zum Bild vor dem Text (optional)
        color
            Die Hintergrundfarbe
        border
            Die Rahmenfarbe

        Returns
            Das erstellte Label
        """
        label = gamegridp.ToolbarLabel(self.width, 25, img_path=img_path, text=text, color=color, border=border)
        label.setup(self)
        self.elements.append(label)
        self.dirty = 1
        return label

    def _elements_height(self):
        height = 0
        for element in self.elements:
            height += element.height
        return height

    def call_click_event(self, button, pos_x, pos_y):
        if button == "mouse_left":
            height = 0
            if not pos_y > self._elements_height():
                for element in self.elements:
                    if height + element.height > pos_y:
                        return element.call_click_event(button, pos_x, pos_y)
                    else:
                        height = height + element.height
        else:
            return "no toolbar event"




