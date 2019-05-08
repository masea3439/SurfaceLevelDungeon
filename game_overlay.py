from typing import List, Dict
import pygame
import os


class Sidebar:
    """Contains list of buildings and information to draw sidebar

    === Public Attributes ===
    building_info:
        Dictionary that stores building names and sprites
    """
    #building_info: Dict[str: pygame.image]

    def __init__(self, building_names: List[str]) -> None:
        self.building_info = {}
        for name in building_names:
            image = pygame.image.load(os.path.join(os.path.dirname(__file__), 'images\\' + name + '.png'))
            self.building_info[name] = image