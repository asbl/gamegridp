from gamegridp import actor
import gamegridp


class MyGrid(gamegridp.CellGrid):
    """My Grid with custom setup method."""
    def setup(self):
        self.robot1 = Robot(grid=self, position=(0, 0))
        self.robot1.add_image("images/robo_green.png")
        self.robot2 = Robot(grid=self, position=(28, 0))
        self.robot2.add_image("images/robo_yellow.png")
        self.robot2.turn_left(180)
        self.add_image(img_path = "images/water.png")

    def act(self):
        pass


class Explosion(actor.Actor):
    def setup(self):
        self.add_image("images/explosion.png")


class Robot(actor.Actor):
    def setup(self):
        self.image_actions.append("scale")

    def act(self):
        self.move()

    def get_event(self, event, data):
        if event == "collision":
            position = self.position
            explosion = Explosion(grid=self.grid, position=position)
            self.grid.add_actor(explosion)
            for actor in data:
                actor.remove()



my_grid = MyGrid("My Grid", cell_size=40, columns=29, rows=1,
                margin=0,)
my_grid.speed = 50
my_grid.show()
