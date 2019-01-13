from gamegridp import gamegrid
import pygame

class PixelGrid(gamegrid.GameGrid):
    """
    Das Pixel-Grid ist gedacht für Grids, deren Zellen genau 1 Pixel groß sind, d.h.
    für Spiele in denen Pixelgenaue Informationen wichtig sind.
    """

    def __init__(self, title, **kwargs):
        super().__init__(title, **kwargs)


    def _init_collisions(self):
        self._collision_partners = dict
        self._last_collisions = set()

    def add_collision_partner(self, partner1, partner2):
        partner1.add_collision_partner(partner2)
        partner2.add_collision_partner(partner1)

    def _call_collision_events(self):
        new_col_pairs = []
        for partner1 in self.actors:
            collisions = pygame.sprite.spritecollide(partner1, partner1.collision_partners, False)
            for partner2 in collisions:
                if (partner1, partner2) not in self._last_collisions:
                    partner1.listen("collision",partner2)
                new_col_pairs.append((partner1, partner2))
        self._last_collisions = set(new_col_pairs)

    def test_collision(self, actor1, actor2) -> bool:
        if actor1 is not actor2:
            print(actor1)
            print(actor1.grid)
            if actor1.rect.colliderect(actor2.rect):
                return True
            else:
                return False

    def destination_is_at_border(self, destination, actor):
        """
        Überprüfe, ob das Rechteck über den entsprechenden Rand hinausragt

        :param rect: Das Rechteck, dass überprüft werden soll.
        :param border: Der Rand, der überprüft werden soll.
        :return: True, falls Ja, ansonsten False
        """
        borders = []
        rect = actor.rect
        rect = self.map_rect_to_cell(destination, actor.rect)
        if rect.topleft[0] <= 0:
            borders.append("left")
        if rect.topleft[1] + rect.height >= self.container_height:
            borders.append("bottom")
        if rect.topleft[0] + rect.width >= self.container_width:
            borders.append("right")
        if rect.topleft[1] <= 0:
            borders.append("top")
        return borders

    def is_at_border(self, actor):
        borders = self.destination_is_at_border(actor.cell, actor)
        if borders:
            return True
        else:
            return False

    def get_touching_borders(self, actor) -> list:
        borders = self.destination_is_at_border(actor.cell, actor)
        return borders

    def destination_is_in_grid(self, destination, actor):
        rect = actor.rect
        if rect.topleft[0] < 0:
            return False
        if rect.topleft[1] < 0:
            return False
        if rect.topleft[0] + rect.width > self.container_width:
            return False
        if rect.topleft[1] + rect.height > self.container_height:
            return False  # rectangle is not in grid
        else:
            return True  # rectangle is in grid

    def is_in_grid(self, actor):
        return(self.destination_is_in_grid(actor.cell, actor))

    def is_valid_move(self, destination_cell, actor = None):
        if not self.is_in_grid(destination_cell, actor):
            return False
        return True
