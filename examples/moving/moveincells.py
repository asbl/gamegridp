from gamegridp import *
import logging

class MyGrid(CellGrid):

    def __init__(self):
        super().__init__(cell_size=40, columns=15, rows=5, margin=1)
        player1 = Player()
        self.add_actor(player1, position=(0, 0))
        self.add_image("images/soccer_green.jpg")


class Player(Actor):
    def __init__(self):
        super().__init__()
        self.size=(40,40)
        self.add_image(img_path="images/char_blue.png",)
        self.image_action("show_overlay", True)

    def act(self):
        if self.grid.is_in_grid(self.look(direction = "forward")):
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

logging.basicConfig(level = logging.INFO)
my_grid = MyGrid()
my_grid.speed = 50
my_grid.show()
