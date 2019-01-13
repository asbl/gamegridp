import pygame
import gamegridp
from gamegridp import keys
import os


class GameGridWindow:
    def __init__(self, title):
        self.title = title
        self.__containers = []
        self._quit = False
        self.dirty = 1
        self.repaint_areas = []
        self.window_surface = pygame.display.set_mode((self.x_res, self.y_res))
        pygame.display.set_caption(title)

    def show(self):
        self.window_surface = pygame.display.set_mode((self.x_res, self.y_res))
        while not self._quit:
            self.update()

    def update(self):
        self.send_pygame_events()
        self.repaint_areas = []
        if self.dirty:
            self.repaint_areas.append(pygame.Rect(0, 0, self.x_res, self.y_res))
        for container in self.__containers:
            container.update()
            container.repaint()
            container.blit_surface_to_window_suface()
        pygame.display.update(self.repaint_areas)
        self.repaint_areas = []

    def add_container(self, container, docking_position):
        container.add_to_window(self, docking_position)
        self.__containers.append(container)

    def remove_container(self, container):
        self.__containers.remove(container)

    def reset(self):
        """
        Entfernt alle Akteure aus dem Grid und setzt sie an ihre Ursprungspositionen.
        """
        for container in self.__containers:
            container.remove()
            self.remove_container(container)

    @property
    def x_res(self):
        containers_width = 0
        for container in self.__containers:
            if container.window_docking_position == "top_left":
                containers_width = container.width
            elif container.window_docking_position == "right":
                containers_width += container.width
        return containers_width

    @property
    def y_res(self):
        containers_height = 0
        for container in self.__containers:
            if container.window_docking_position == "top_left":
                containers_height = container.height
            elif container.window_docking_position == "bottom":
                containers_height += container.height
        return containers_height

    def get_container_by_pixel(self, pixel_x: int, pixel_y: int):
        for container in self.__containers:
            print(pixel_x, pixel_y)
            if container.rect().collidepoint((pixel_x, pixel_y)):
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
                print("key down!!!")
                self.send_event_to_containers("key_down", keys.key_codes_to_keys(keys_pressed))
        if pygame.key.get_pressed().count(1) != 0:
            keys_pressed = pygame.key.get_pressed()
            self.send_event_to_containers("key", keys.key_codes_to_keys(keys_pressed))
            self.send_event_to_containers("key_pressed", keys.key_codes_to_keys(keys_pressed))
        mouse_x, mouse_y = pygame.mouse.get_pos()
        return False

    def send_event_to_containers(self, event, data):
        for container in self.__containers:
            print("send event:", event, "to container", container)
            container.pass_event(event, data)
            container.get_event(event,data)

    def _call_quit_event(self):
        self._quit = True
        pygame.quit()
        os._exit(0)
