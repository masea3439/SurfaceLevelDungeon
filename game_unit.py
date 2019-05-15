import pygame
import os
#from game_map import Tile


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

    def move_update(self, tile) -> None:
        pass


class Worker(Unit):
    def __init__(self) -> None:
        Unit.__init__(self, 'worker_test')


class Lich(Unit):
    def __init__(self) -> None:
        Unit.__init__(self, 'lich')

    def move_update(self, tile) -> None:
        if not tile.corrupted:
            tile.corrupted = True
            if tile.resources == [('life', 2)]:
                tile.create_animation([pygame.image.load(os.path.join(os.path.dirname(__file__), 'images\\life.png'))], 60)
            elif tile.resources == [('stratum', 3)]:
                tile.create_animation([pygame.image.load(os.path.join(os.path.dirname(__file__), 'images\\stratum.png'))], 60)

            tile.resources = []
