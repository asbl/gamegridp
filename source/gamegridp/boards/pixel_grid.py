from gamegridp.boards import *
from gamegridp.actors import *
import pygame

class PixelGrid(GameGrid):

    def __init__(self, cell_size=1, columns=40, rows=40, margin=0):
        super().__init__(cell_size=cell_size, columns=columns, rows=rows, margin=margin)
        self._collision_parnters_dict = dict()
        self._collision_partners = dict
        self._last_collisions = set()

    def add_collision_partner(self, partner1, partner2):
        self._collision_parnters_dict[partner1.actor_id].add(partner2)
        self._collision_parnters_dict[partner2.actor_id].add(partner1)

    def add_actor(self, actor: Actor, position) -> Actor:
        """
        Overwrites add_actor in gamegrid
        :param actor: The actors to be added
        :param position: The position where the actors should be placed in the boards
        :return: The reference to the Actor object
        """
        super().add_actor(actor, position)
        if actor.size == (0, 0):
            actor.size = (30, 30)
        self._collision_parnters_dict[actor.actor_id] = pygame.sprite.Group()
        return actor

    def remove_actor(self, actor : Actor):
        actor_id = actor.actor_id
        del self._collision_parnters_dict[actor_id]
        super().remove_actor(actor)



    def _call_collision_events(self):
        new_col_pairs = []
        for partner1 in self.actors:
            if partner1.actor_id in  self._collision_parnters_dict:
                collisions = pygame.sprite.spritecollide(partner1,
                                                         self._collision_parnters_dict[partner1.actor_id], False)
                if collisions:
                    print(collisions)
                for partner2 in collisions:
                    if (partner1, partner2) not in self._last_collisions:
                        partner1.listen("collision",partner2)
                    new_col_pairs.append((partner1, partner2))
                for pair in new_col_pairs:
                    self.window.send_event_to_containers("collision", pair)
        self._last_collisions = set(new_col_pairs)



    def test_collision(self, actor1, actor2) -> bool:
        if actor1 is not actor2:
            if actor1.rect.colliderect(actor2.rect):
                return True
            else:
                return False

    def is_at_border(self, rect):
        """
        Überprüfe, ob das Rechteck über den entsprechenden Rand hinausragt

        :param rect: Das Rechteck, dass überprüft werden soll.
        :param border: Der Rand, der überprüft werden soll.
        :return: True, falls Ja, ansonsten False
        """
        borders = []
        if rect.topleft[0] <= 0:
            borders.append("left")
        if rect.topleft[1] + rect.height >= self.height:
            borders.append("bottom")
        if rect.topleft[0] + rect.width >= self.width:
            borders.append("right")
        if rect.topleft[1] <= 0:
            borders.append("top")
        return borders

    def get_touching_borders(self, rect) -> list:
        borders = []
        if rect.topleft[0] <= 0:
            borders.append("left")
        if rect.topleft[1] + rect.height >= self.height:
            borders.append("bottom")
        if rect.topleft[0] + rect.width >= self.width:
            borders.append("right")
        if rect.topleft[1] <= 0:
            borders.append("top")
        return borders
