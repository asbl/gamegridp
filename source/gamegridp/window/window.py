import pygame
import logging
from gamegridp.tools import keys
import os


class GameGridWindow:

    log = logging.getLogger("Window")

    def __init__(self, title):
        self.title = title
        self._containers = []
        self._quit = False
        self.dirty = 1
        self.repaint_areas = []
        self.window_surface = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption(title)

    def show(self):
        self.window_surface = pygame.display.set_mode((self.window_width, self.window_height))
        while not self._quit:
            self.update()

    def update(self):
        self.send_pygame_events()
        self.repaint_areas = []
        if self.dirty:
            self.repaint_areas.append(pygame.Rect(0, 0, self.window_width, self.window_height))
        for container in self._containers:
            container.update()
            container.repaint()
            container.blit_surface_to_window_surface()
        pygame.display.update(self.repaint_areas)
        self.repaint_areas = []

    def add_container(self, container, dock):
        self._containers.append(container)
        container.add_to_window(self, dock)

    def remove_container(self, container):
        self._containers.remove(container)

    def reset(self):
        """
        Entfernt alle Akteure aus dem Grid und setzt sie an ihre Ursprungspositionen.
        """
        for container in self._containers:
            container.remove()
            self.remove_container(container)

    @property
    def window_width(self):
        containers_width = 0
        for container in self._containers:
            if container.window_docking_position == "top_left":
                containers_width = container.width
            elif container.window_docking_position == "right":
                containers_width += container.width
            elif container.window_docking_position == "main":
                containers_width = container.width
        return containers_width

    @property
    def window_height(self):
        containers_height = 0
        for container in self._containers:
            if container.window_docking_position == "top_left":
                containers_height = container.height
            elif container.window_docking_position == "bottom":
                containers_height += container.height
            elif container.window_docking_position == "main":
                containers_height = container.height
        return containers_height

    def get_container_by_pixel(self, pixel_x: int, pixel_y: int):
        for container in self._containers:
            if container.rect.collidepoint((pixel_x, pixel_y)):
                return container
        return None

    def send_pygame_events(self):
        for event in pygame.event.get():
            # Event: Quit
            if event.type == pygame.QUIT:
                self._call_quit_event()
            # Event: Mouse-Button Down
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                container = self.get_container_by_pixel(pos[0], pos[1])
                if event.button == 1:
                    container.get_event("mouse_left", (pos[0], pos[1]))
                if event.button == 3:
                    container.get_event("mouse_right", (pos[0], pos[1]))
            elif event.type == pygame.KEYDOWN:
                # key-events
                keys_pressed = pygame.key.get_pressed()
                self.send_event_to_containers("key_down", keys.key_codes_to_keys(keys_pressed))
        if pygame.key.get_pressed().count(1) != 0:
            keys_pressed = pygame.key.get_pressed()
            self.send_event_to_containers("key", keys.key_codes_to_keys(keys_pressed))
            self.send_event_to_containers("key_pressed", keys.key_codes_to_keys(keys_pressed))
        return False

    def send_event_to_containers(self, event, data):
        self.log.info("Send event '{0}' with key list: {1}".format(event, data))
        for container in self._containers:
            container.pass_event(event, data)
            container.get_event(event,data)

    def _call_quit_event(self):
        self._quit = True
        pygame.quit()
        os._exit(0)
