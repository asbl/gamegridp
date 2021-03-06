import pygame
import math
import logging
import sys


class ImageRenderer():
    """
    Utility class for managing sprite images
    """
    log = logging.getLogger("image_renderer")
    images_dict = {}

    def __init__(self):
        # not mutable
        self._images_list = []  # Original images
        self._image_paths = []
        self._image_index = 0 # current_image index (for animations)
        self.image_actions = {"flip" : True, "rotate" : True, "scale_x" : True, "scale_y" : True, "info_overlay": False, "center" : False, "grid_overlay": False}
        self.direction = 0
        self.size = (0,0)
        self.margin = 0
        self.cell_size = 0
        self.orientation = 0
        self.flipped = True

    def add_image(self, img_path: str) -> pygame.Surface:
        """
        adds an image
        :param img_path:  the image path
        :return: the image added
        """
        if img_path in ImageRenderer.images_dict :
            # load image from img_dict
            _image = ImageRenderer.images_dict[img_path]
        else :
            # create new image and add to img_dict
            _image = pygame.image.load(img_path).convert_alpha()
            ImageRenderer.images_dict[img_path] = _image
        self._images_list.append(_image)
        self._image_paths.append(img_path)
        return _image

    def load_image_by_index(self, index):
        if self.image_actions["info_overlay"] is True:
            image = pygame.image.load(self._image_paths[index]).convert_alpha()
        else:
            image = self._images_list[self._image_index]
        return image

    def get_image(self) -> pygame.Surface:
        try:
            if self._images_list:
                image = self.load_image_by_index(self._image_index)
            else:
                image = pygame.Surface((1,1))
            image = self.rotate_image(image, self.orientation)
            if self.image_actions["info_overlay"] is True:
                image = self.info_overlay(image, (255, 0, 0))
            if self.image_actions["grid_overlay"] is True:
                image = self.grid_overlay(image, self.size[0], self.size[1], self.cell_size, self.cell_size, self.margin)
            if self.image_actions["scale_x"] is True:
                image = self.scale_x_image(image, self.size[0])
            if self.image_actions["scale_y"] is True:
                image = self.scale_y_image(image, self.size[1])
            if self.image_actions["center"] is True:
                image = self.center_image(image, self.size[0])
            if self.image_actions["flip"] is True:
                image = self.flip_image(image, self.flipped, False)
            if self.image_actions["rotate"] is True:
                image = self.rotate_image(image, self.direction)
            return image
        except KeyError as e:
            self.log.error("Invalid  value for image_action in ImageRenderer")
            sys.exit(1)

    def flip_image(self, image, flip_x : bool, flip_y : bool) -> pygame.Surface:
        return pygame.transform.flip(image, flip_y, flip_x)

    def rotate_image(self, image, direction):
        return pygame.transform.rotate(image, direction)

    def scale_x_image(self, image, size):
        return pygame.transform.scale(image, (size, image.get_height()))

    def scale_y_image(self, image, size):
        return pygame.transform.scale(image, (image.get_width(), size))

    def upscale_image(self, image, size):
        if image.get_width() < size[0] or image.get_height() < size[1]:
            ImageRenderer.scale_image(image, size)

    def center_image(self, image, size):
        cropped_surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
        width = image.get_width()
        height = image.get_height()
        x_pos = (size - width) / 2
        y_pos = (size - height) / 2
        cropped_surface.blit(image, (x_pos, y_pos), (0, 0, size, size))
        return cropped_surface

    def crop_image(self, image, size):
        cropped_surface = pygame.Surface(size)
        cropped_surface.fill((255, 255, 255))
        cropped_surface.blit(image, (0, 0),(0, 0, size[0], size[1]))
        return cropped_surface

    def info_overlay(self, image, color):
        pygame.draw.rect(image, color,
                         (0, 0, image.get_rect().width, image.get_rect().height), 10)
        # draw direction marker on image
        rect = image.get_rect()
        center = rect.center
        x = rect.right
        y = rect.centery
        pygame.draw.line(image, color, (center[0], center[1]), (x, y))
        return image

    @staticmethod
    def grid_overlay(image, width, height, cell_width, cell_height, cell_margin, color = (255, 0, 0)):
            i = 0
            while i <= width:
                pygame.draw.rect(image, color,[i, 0, cell_margin, height])
                i += cell_height + cell_margin
            i = 0
            while i <= height:
                pygame.draw.rect(image, color, [0, i, width, cell_margin])
                i += cell_width + cell_margin
            return image

    @staticmethod
    def set_text(self, image, text, size):
        my_font = pygame.font.SysFont("monospace", size)
        label = my_font.render(text, 1, (0, 0, 0))
        image.blit(label, (0, 0))
        self.__images_list[0] = self.image

    def delete_images(self):
        """
        Löscht alle Bilder eines Akteurs. Dies kann z.B. sinnvoll sein,
        wenn eine neue Animation festgelegt werden soll und dafür die alte
        Animation zuvor gelöscht werden muss.
        """
        self._images_list = []

    def next_sprite(self):
        if self._image_index < self._images_list.__len__() - 1:
            self._image_index = self._image_index + 1
        else:
            self._image_index = 0
