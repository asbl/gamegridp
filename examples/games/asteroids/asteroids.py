import gamegridp
from gamegridp import keys
import random
import sys

class MyGrid(gamegridp.PixelGrid):
    """My Grid with custom setup method."""

    def setup(self):
        asteroids = list()
        for i in range(5):
            asteroid=Asteroid(grid=self, cell=(random.randint(30,screen_x-30),random.randint(0+30,screen_y-30)))
            asteroids.append(asteroid)
        self.set_background("images/galaxy.jpg","scale")
        player1 = Player(grid=self, cell=(40, 40))
        for asteroid in asteroids:
            player1.add_collision_partner(asteroid)

    def listen(self, event, data):
        if event == "collision":
            partner1, partner2 = data[0], data[1]
            Explosion(grid=self, cell=partner1.cell)
            partner1.remove()
            partner2.remove()
            self.stop()


class Player(gamegridp.Actor):

    def setup(self):
        self.add_image("images/ship.png","scale",(30,30))
        self.set_rotatable()


    def listen(self,event,data):
        if event == "key":
            if "W" in data:
                self.turn_left(10)
            elif "S" in data:
                self.turn_right(10)

    def act(self):
        self.move(3)


class Asteroid(gamegridp.Actor):
    def setup(self):
        self.set_image("images/asteroid.png","scale",(30,30))
        self.set_rotatable()
        self.direction = random.randint(0, 360)


    def act(self):
        valid = self.move(4)
        if not valid:
            self.turn_left(180)

class Explosion(gamegridp.Actor):
    def setup(self):
        self.add_image("images/explosion.png", "do_nothing")

random.seed()
screen_x=400
screen_y=300
MyGrid.log()
mygrid = MyGrid("My Grid", cell_size=1, columns=screen_x, rows=screen_y,
                margin=0, speed=60)
mygrid.show()
