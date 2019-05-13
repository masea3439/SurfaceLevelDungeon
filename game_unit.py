import pygame
import os


class Unit:
    """Unit on the game map

    === Public Attributes ===
    unit_image:
        Sprite of the unit
    unit_image_h:
        Sprite of the unit while selected
    selected:
        If this unit is selected
    """

    unit_image: pygame.image
    unit_image_h: pygame.image
    selected: bool

    def __init__(self, unit_name: str) -> None:
        self.unit_image = pygame.image.load(os.path.join(os.path.dirname(__file__), 'images\\' + unit_name + '.png'))
        self.unit_image_h = pygame.image.load(os.path.join(os.path.dirname(__file__), 'images\\' + unit_name + '_h.png'))
        self.selected = False
