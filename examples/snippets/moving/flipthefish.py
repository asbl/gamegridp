import logging
import sys
import gamegridp


class MyGrid(gamegridp.CellGrid):
    """My Grid with custom setup method."""
    def setup(self):
        self.player1 = Player(grid=self, position = (3, 3))
        self.add_image("images/water.png")


class Player(gamegridp.Actor):
    def setup(self):
        self.add_image(img_path="images/fish.png")

    def act(self):
        if self.grid.is_in_grid(self.look_forward()):
            self.move()
        else:
            self.flip_x()


my_grid = MyGrid("My Grid", cell_size=25, columns=10, rows=5,
                margin=1,)
my_grid.speed = 50
my_grid.show()
