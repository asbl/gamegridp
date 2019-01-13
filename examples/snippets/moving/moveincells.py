import gamegridp
from gamegridp import keys
import logging
import sys

class MyGrid(gamegridp.CellGrid):
    """My Grid with custom setup method."""

    def setup(self):
        self.player1 = Player(grid=self, position=(3, 3))
        self.add_image("images/soccer_green.jpg")
        self.player1.add_image(img_path="images/char_blue.png",)


class Player(gamegridp.Actor):
    def setup(self):
        pass

    def act(self):
        if self.grid.is_in_grid(self.look_forward()):
            self.move()

    def get_event(self, event, data):
        if event == "key_down":
            if "W" in data:
                self.direction = "up"
            elif "S" in data:
                self.direction = "down"
            elif "A" in data:
                self.direction = "left"
            elif "D" in data:
                self.direction = "right"


my_grid = MyGrid("My Grid", cell_size=40, columns=15, rows=5, margin=1)
my_grid.speed = 50
my_grid.show()
