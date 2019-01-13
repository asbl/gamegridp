import gamegridp


class MyGrid(gamegridp.CellGrid):
    """My Grid with custom setup method."""
    def setup(self):
        self.add_image("images/water.png")
        self.player1 = Robot(grid=self, position=(50, 70))


class Robot(gamegridp.Actor):

    def setup(self):
        self.add_image("images/robot_blue1.png")
        self.add_image("images/robot_blue2.png")
        self.animation_speed = 30
        self.animate()

    def act(self):
        if self.grid.is_in_grid(self.look_forward()):
            self.move()
        else:
            self.flip_x()


my_grid = MyGrid("My Grid", cell_size=1, columns=500, rows=150, margin=0)
# my_grid.window.add("actionbar")
my_grid.show()
