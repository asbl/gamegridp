import gamegridp
from gamegridp import keys
import random
import sys

class MyGrid(gamegridp.PixelGrid):
    """My Grid with custom setup method."""

    def setup(self):
        self.set_background("images/galaxy.jpg","scale")
        self.add_container(gamegridp.EventConsole())
        self.add_container(gamegridp.ActorToolbar(size=200))
        asteroids=[]
        for i in range(1):
            #new_asteroid = Asteroid(grid=self, cell=(random.randint(35,self.columns-35),random.randint(35,self.rows-35)))
            new_asteroid = Asteroid(grid=self,
                                    cell=(random.randint(35, self.columns - 35), random.randint(35, self.rows - 35)))
            for asteroid in asteroids:
                self.add_collision_partner(new_asteroid, asteroid)
            asteroids.append(new_asteroid)

    def listen(self, event, data):
        if event == "collision":
            partner1, partner2 = data[0], data[1]
            pass



class Asteroid(gamegridp.PhysicsActor):
    def setup(self):
        self.set_image("images/asteroid.png","scale",(30,30))
        self.set_rotatable()
        self.direction = random.randint(0, 360)
        self.set_bounding_box_size((30, 30))
        self.bounce_from_borders = True

    def act(self):
        self.move()

    def listen(self, event, data):
        if event == "border-event" and data:
            self.bounce_from_border()

random.seed()
mygrid = MyGrid("My Grid", cell_size=1, columns=400, rows=400, margin=0)
mygrid.log()
mygrid.show()

