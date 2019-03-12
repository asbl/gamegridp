from gamegridp import *


class MyGrid(CellGrid):

    def __init__(self):
        super().__init__(cell_size=42, columns=20, rows=8, margin=1)
        self.add_image(img_path="images/soccer_green.jpg")
        player1 = Player( )
        self.add_actor(player1, position=(3, 3))
        player2 = Player()
        self.add_actor(player2, position=(8, 2))


class Player(Actor):
    def __init__(self):
        super().__init__()
        self.add_image(img_path="images/char_blue.png")

    def act(self):
        if not self.grid.is_in_grid(self.look("forward")):
            self.turn_left(90)
        self.move()


my_grid = MyGrid()
my_grid.speed = 40
my_grid.show()
