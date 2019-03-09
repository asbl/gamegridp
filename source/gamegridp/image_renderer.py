import pygame
import math


class ImageRenderer():
    """
    Utility class for managing sprite images
    """

    images_dict = {}

    def __init__(self):
        # not mutable
        self._images_list = []  # Original images
        self._image_index = 0 # current_image index (for animations)

    def add_image(self, img_path: str):
        """
        adds an image
        :param img_path:  the image path
        :return: the image added
        """
        if img_path in ImageRenderer.images_dict:
            # load image from img_dict
            _image = ImageRenderer.images_dict[img_path]
        else :
            # create new image and add to img_dict
            _image = pygame.image.load(img_path).convert_alpha()
            ImageRenderer.images_dict[img_path] = _image
        self._images_list.append(_image)
        return _image

    def get_image(self):
        """
        gets actual image
        :return: the actual image
        """
        if self._images_list:
            return self._images_list[self._image_index]
        else:
            _image = pygame.Surface((1,1))
            return _image

    @staticmethod
    def flip_image(image, flip_x, flip_y):
        return pygame.transform.flip(image, flip_y, flip_x)

    @staticmethod
    def rotate_image(image, direction):
        return pygame.transform.rotate(image, direction)

    @staticmethod
    def scale_image(image, size):
        return pygame.transform.scale(image, (size[0], size[1]))

    @staticmethod
    def upscale_image(image, size):
        if image.get_width() < size[0] or image.get_height() < size[1]:
            ImageRenderer.scale_image(image, size)

    @staticmethod
    def center_image(image, size, cell_size):
        cropped_surface = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA, 32)
        width = image.get_width()
        height = image.get_height()
        x_pos = (cell_size - width) / 2
        y_pos = (cell_size - height) / 2
        cropped_surface.blit(image, (x_pos, y_pos), (0, 0, cell_size, cell_size))
        return cropped_surface

    @staticmethod
    def crop_image(image, size):
        cropped_surface = pygame.Surface(size)
        cropped_surface.fill((255, 255, 255))
        cropped_surface.blit(image, (0, 0),(0, 0, size[0], size[1]))
        return cropped_surface

    @staticmethod
    def draw_direction_overlay(image, color, direction):
        pygame.draw.rect(image, color,
                         (0, 0, image.get_width(), image.get_height()), 2)
        # draw direction marker on image
        center_x = image.get_width() / 2
        center_y = image.get_height() / 2
        x = round(image.get_width() / 2 + math.cos(math.radians(direction))
                  * image.get_width())
        y = round(image.get_height() / 2 - math.sin(math.radians(direction))
                  * image.get_height())
        pygame.draw.line(image, color, (center_x, center_y), (x, y), width = 2)

    @staticmethod
    def draw_grid_overlay(image, width, height, cell_width, cell_height, color, cell_margin):
            i = 0
            while i <= width:
                pygame.draw.rect(image, color,[i, 0, cell_margin, height])
                i += cell_height + cell_margin
            i = 0
            while i <= height:
                pygame.draw.rect(image, color, [0, i, width, cell_margin])
                i += cell_width + cell_margin

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
