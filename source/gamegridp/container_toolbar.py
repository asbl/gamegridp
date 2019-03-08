import gamegridp


class Toolbar(gamegridp.Container):

    def __init__(self, size=100):
        super().__init__(size)
        self.width = size
        self.widgets = []
        self.dirty = 1
        self.position = "right"

    def get_widget(self, index):
        return self.widgets[index]

    def add_widget(self, widget):
        widget.width = self.width
        widget.height = 25
        widget.clear()
        self.widgets.append(widget)

    def _draw_surface(self, surface):
        """
        Creates a toolbar on the left side of the window
        """
        _actual_height = 0
        for widget in self.widgets:
            if widget.dirty == 1:
                widget.repaint()
                surface.blit(widget.surface, (0, _actual_height))
                widget.dirty = 0
            _actual_height = _actual_height + widget.height

    def _widgets_total_height(self):
        height = 0
        for widget in self.widgets:
            height += widget.height
        return height

    def call_click_event(self, button, pos_x, pos_y):
        if button == "mouse_left":
            height = 0
            if not pos_y > self._widgets_total_height():
                for widget in self.widgets:
                    if height + widget.height > pos_y:
                        return widget.call_click_event(button, pos_x, pos_y)
                    else:
                        height = height + widget.height
        else:
            return "no toolbar event"




