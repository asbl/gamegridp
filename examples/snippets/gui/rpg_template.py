import gamegridp


class MyGrid(gamegridp.CellGrid, gamegridp.GUIGrid):
    def setup(self):
        Wall(self, (0, 4))
        Grass(self, (0, 2))
        Player(self, (0, 0))
        self.toolbar.add_button("Watch")


class Wall(gamegridp.Actor):
    def setup(self):
        self.is_blocking = True
        self.set_image("images/wall.png")


class Grass(gamegridp.Actor):
    def setup(self):
        self.set_image("images/grass.png")


class Player(gamegridp.Actor):
    def setup(self):
        self._is_rotatable = False
        self.set_image("images/knight.png")
        self.inventory = []

    def act(self):
        pass

    def listen(self, event, data):
        if event == "key_down":
            if "W" in data:
                self.move_up()
            elif "S" in data:
                self.move_down()
            elif "A" in data:
                self.move_left()
            elif "D" in data:
                self.move_right()
            grass = self.get_actor_at_my_location("Grass")
            if grass:
                self.grid.console.print("Du läufst über eine Wiese")
        elif event == "button" and data == "Watch":
            actor = self.get_actor_at_my_location("Grass")
            if actor is not None and actor.class_name == "Grass":
                self.grid.console.print("Du siehst eine Wiese")


MyGrid.log()
mygrid = MyGrid("My Grid", cell_size=40, columns=10, rows=10,
                margin=1, console=True, toolbar=True)
mygrid.show()
