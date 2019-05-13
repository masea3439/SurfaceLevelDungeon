import pygame
import os


class Building:
    """Building on the game map

    === Public Attributes ===
    building_image:
        Sprite of the building
    building_image_h:
        Sprite of the building while selected
    selected:
        If this building is selected
    """

    building_image: pygame.image

    def __init__(self, building_name: str) -> None:
        self.building_image = pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'images\\' + building_name + '.png'))
        self.building_image_h = pygame.image.load(
            os.path.join(os.path.dirname(__file__), 'images\\' + building_name + '_h.png'))
        self.selected = False
