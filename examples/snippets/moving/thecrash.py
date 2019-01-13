from gamegridp import actor
import gamegridp


class MyGrid(gamegridp.CellGrid):
    """My Grid with custom setup method."""
    def setup(self):
        self.robot1 = Robot(grid=self, cell=(0, 0))
        self.robot1.add_image("images/robo_green.png")
        self.robot2 = Robot(grid=self, cell=(28, 0))
        self.robot2.add_image("images/robo_yellow.png")
        self.robot1.add_collision_partner(self.robot2)
        self.robot2.turn_left(180)
        self.add_image(img_path = "images/water.png")

    def act(self):
        pass

    def collision(self, partner1, partner2):
        cell = self.robot1.get_cell()
        explosion = Explosion(title="boom", grid=self, location=self.robot1.location)
        self.remove_actor(self.robot1)
        self.remove_actor(self.robot2)
        self.add_actor(explosion)

class Explosion(actor.Actor):
    def setup(self):
        self.add_image("images/explosion.png")


class Robot(actor.Actor):
    def setup(self):
        self.set_rotatable()

    def act(self):
        self.move()


mygrid = MyGrid("My Grid", cell_size=40, columns=29, rows=1,
                margin=0,)
mygrid.show()
