import os
import gamegridp
import pygame


class ActorToolbar(gamegridp.Toolbar):

    def __init__(self, size=100):
        super().__init__(size)
        self.position = "right"
        self.actor = None
        self._init_labels()

    def _init_labels(self):
        self.label_id = self.add_label(text="ID")
        self.label_direction = self.add_label(text="Direction")
        self.label_border = self.add_label(text="Is at Border")
        self.label_borders = self.add_label(text="Borders")
        self.label_grid = self.add_label(text="Is in grid")
        self.colliding = self.add_label(text="Colliding")
        self.colliding_actors = self.add_label(text="colliding_actors")

    def listen(self, event, data):
        if event == "active_actor":
            print("action-toolbar: active-actor event")
            self.actor = data
            self.label_id.set_text("ID:" + str(self.actor.id))
            self.label_direction.set_text("Direction:"+str(self.actor.direction))
            self.label_border.set_text("Is at Border:" + str(self.actor.is_at_border))
            self.label_grid.set_text("Is in Grid:" + str(self.actor.is_in_grid))
        if event == "out of grid" and data == self.actor:
            self.label_grid.set_text("Is in Grid:" + str(self.actor.is_in_grid))
        if event == "border-event" and data == self.actor:
            print("is_At_border")
            self.label_border.set_text("is at Border:" + str(self.actor.is_at_border))
            self.label_borders.set_text("Borders:" + str(self.actor.touching_borders))
            self.label_direction.set_text("Direction:" + str(self.actor.direction))

    def reset(self):
        super().reset()
        self._init_labels()
