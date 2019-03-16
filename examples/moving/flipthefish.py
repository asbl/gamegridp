from gamegridp import *


class MyGrid(CellGrid):

    def __init__(self):
        super().__init__(cell_size=50, columns=10, rows=1, margin=1)
        player1 = Player()
        self.add_actor(player1, position=(0, 0))
        self.add_image("images/water.png")


class Player(Actor):

    def __init__(self):
        super().__init__()
        self.add_image(img_path="images/fish.png")

    def act(self):
        if self.grid.is_in_grid(self.look(direction = "forward")):
            self.move()
        else:
            self.flip_x()


my_grid = MyGrid()
my_grid.speed = 50
my_grid.show()
