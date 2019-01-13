import gamegridp

class MyGrid(gamegridp.CellGrid):
    """My Grid with custom setup method."""

    def setup(self):
        self.add_image(img_path="images/soccer_green.jpg")
        player1 = Player(grid=self, position=(3, 3))
        player2 = Player(grid=self, position=(8, 2))


class Player(gamegridp.Actor):
    def setup(self):
        self.add_image(img_path="images/char_blue.png")

    def act(self):
        if not self.grid.is_in_grid(self.look_forward()):
            self.turn_left(90)
        self.move()


my_grid = MyGrid("My Grid", cell_size=16, columns=40, rows=16, margin=1)
my_grid.show()
