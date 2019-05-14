import pygame
from game_map import Grid, Tile
from typing import Tuple, Optional
from game_unit import Unit
from game_overlay import Sidebar
import os
import time


class Visualizer:
    """A class that creates and updates the screen

    === Public Attributes ===
    width:
        Width of the display
    height:
        Height of the display
    grid:
        Object that stores map information
    sidebar:
        Object that stores a list of building names and sprites
    screen:
        !!!!!
    highlight_screen:
        Screen that is slightly transparent
    sprite_frame:
        Which frame of the sprite to draw
    spawn_tile:
        Tile where the player spawns
    life_image:
        Image of the life resource icon
    stratum_image:
        Image of the stratum resource icon
    """

    width: int
    height: int
    grid: Grid
    sidebar: Sidebar
    screen: pygame.Surface
    highlight_screen: pygame.Surface
    highlight_image: pygame.image
    sprite_frame: int
    spawn_tile: Tile
    life_image: pygame.image
    stratum_image: pygame.image
    one: pygame.image
    two: pygame.image
    three: pygame.image

    def __init__(self, width: int, height: int, grid: Grid, sidebar: Sidebar, spawn_tile: Tile) -> None:
        self.game_running = True
        self.width = width
        self.height = height
        self.grid = grid
        self.sidebar = sidebar
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.sprite_frame = 0
        self.spawn_tile = spawn_tile
        #self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        self.life_image = pygame.image.load(os.path.join(os.path.dirname(__file__), 'images\\life.png'))
        self.stratum_image = pygame.image.load(os.path.join(os.path.dirname(__file__), 'images\\stratum.png'))

        self.one = pygame.image.load(os.path.join(os.path.dirname(__file__), 'images\\1.png'))
        self.two = pygame.image.load(os.path.join(os.path.dirname(__file__), 'images\\2.png'))
        self.three = pygame.image.load(os.path.join(os.path.dirname(__file__), 'images\\3.png'))

        # Create highlight screen
        self.highlight_screen = pygame.Surface((120, 104))
        self.highlight_screen.set_colorkey((0, 0, 0))
        highlight_image = pygame.image.load(os.path.join(os.path.dirname(__file__), 'images\\highlight.png'))
        self.highlight_screen.blit(highlight_image, (0, 0))
        self.highlight_screen.set_alpha(100)

        # Create sidebar background screen
        self.sidebar_background_screen = pygame.Surface((180, 65))
        self.sidebar_background_screen.set_colorkey((0, 0, 0))
        highlight_image = pygame.image.load(os.path.join(os.path.dirname(__file__), 'images\\sidebar_background.png'))
        self.sidebar_background_screen.blit(highlight_image, (0, 0))
        self.sidebar_background_screen.set_alpha(200)

    def render_display(self, mouse_grid_location: Tuple[int, int], mouse_sidebar_location: Optional[int],
                       to_build: Optional[str], update_animations: bool, show_resources: bool) -> None:
        """Render the game to the screen
        """
        """
        if self.go:
            pygame.draw.rect(self.screen, (255, 255, 255), (0, 0, self.width, self.height))
            tile = self.grid.tiles[0][0]
            pygame.draw.lines(self.screen, (0, 0, 0), False, tile.vertices[0:5], 1)
            pygame.draw.lines(self.screen, (0, 0, 0), False,
                              [tile.vertices[0], tile.vertices[5], tile.vertices[4]], 1)
            pygame.image.save(self.screen, 'pygame_hex.png')
            self.go = False
        """
        if update_animations:
            if self.sprite_frame == 1:
                self.sprite_frame = 0
            else:
                self.sprite_frame = 1

        # Wipe the screen
        pygame.draw.rect(self.screen, (0, 0, 255), (0, 0, self.width, self.height))

        # Draw tile sprites
        for sublist in self.grid.tiles:
            for tile in sublist:
                if not tile.is_empty:
                    self.screen.blit(tile.land_image, (tile.vertices[0][0] - 30, tile.vertices[0][1]))
                    if tile.supported_unit is not None:
                        if tile.supported_unit.selected:
                            self.screen.blit(tile.supported_unit.unit_image_h,
                                             (tile.vertices[0][0] - 30, tile.vertices[0][1]))
                        else:
                            self.screen.blit(tile.supported_unit.unit_image,
                                             (tile.vertices[0][0] - 30, tile.vertices[0][1]))
                    elif tile.supported_building is not None:
                        if tile.supported_building.selected:
                            self.screen.blit(tile.supported_building.building_image_h,
                                             (tile.vertices[0][0] - 30, tile.vertices[0][1]))
                        else:
                            self.screen.blit(tile.supported_building.building_image,
                                             (tile.vertices[0][0] - 30, tile.vertices[0][1]))
                    if show_resources:
                        for resource in tile.resources:
                            if resource[0] == 'life':
                                self.screen.blit(self.life_image, (tile.vertices[0][0]+17, tile.vertices[0][1]+39))
                            elif resource[0] == 'stratum':
                                self.screen.blit(self.stratum_image, (tile.vertices[0][0]+17, tile.vertices[0][1]+39))
                            if resource[1] == 1:
                                self.screen.blit(self.one, (tile.vertices[0][0] + 17, tile.vertices[0][1] + 14))
                            elif resource[1] == 2:
                                self.screen.blit(self.two, (tile.vertices[0][0] + 17, tile.vertices[0][1] + 14))
                            elif resource[1] == 3:
                                self.screen.blit(self.three, (tile.vertices[0][0] + 17, tile.vertices[0][1] + 14))
        # Draw tile outlines
        hovered_tile = None
        selected_tile = None
        x = 0
        for sublist in self.grid.tiles:
            y = 0
            for tile in sublist:
                if not tile.is_empty:
                    if tile.highlighted:
                        self.screen.blit(self.highlight_screen, (tile.vertices[0][0] - 30, tile.vertices[0][1]))
                    if tile.selected:
                        selected_tile = tile
                    elif (x, y) == mouse_grid_location and mouse_sidebar_location is None:
                        hovered_tile = tile
                    else:
                        # Use draw lines instead of draw polygon to avoid differently drawn diagonal lines
                        pygame.draw.lines(self.screen, (0, 0, 0), False, tile.vertices[0:5], 1)
                        pygame.draw.lines(self.screen, (0, 0, 0), False,
                                          [tile.vertices[0], tile.vertices[5], tile.vertices[4]], 1)
                y += 1
            x += 1

        if hovered_tile is not None:
            # Use draw lines instead of draw polygon to avoid differently drawn diagonal lines
            pygame.draw.lines(self.screen, (94, 152, 152), False, hovered_tile.vertices[0:5], 1)
            pygame.draw.lines(self.screen, (94, 152, 152), False,
                              [hovered_tile.vertices[0], hovered_tile.vertices[5], hovered_tile.vertices[4]], 1)
        if selected_tile is not None:
            # Use draw lines instead of draw polygon to avoid differently drawn diagonal lines
            pygame.draw.lines(self.screen, (219, 232, 101), False, selected_tile.vertices[0:5], 3)
            pygame.draw.lines(self.screen, (219, 232, 101), False,
                              [selected_tile.vertices[0], selected_tile.vertices[5], selected_tile.vertices[4]], 3)

        # Draw sidebar
        num = 0
        for building in self.sidebar.building_info:
            self.screen.blit(self.sidebar_background_screen, (0, num*65+100))
            rectangle = pygame.Rect(0, num*65+100, 180, 65)
            if num == mouse_sidebar_location:
                pygame.draw.rect(self.screen, (255, 255, 255), rectangle, 2)
            else:
                pygame.draw.rect(self.screen, (85, 0, 111), rectangle, 2)
            if to_build is not None:
                if to_build == building[0]:
                    pygame.draw.rect(self.screen, (219, 232, 101), rectangle, 3)
            self.screen.blit(building[1], (0, num*65+100))
            num += 1

        # update the display
        pygame.display.flip()

    def render_spawning(self, frame: int) -> None:
        image = pygame.image.load(os.path.join(os.path.dirname(__file__), 'images\\sprite_' + str(frame) + '.png'))
        self.screen.blit(image, (self.spawn_tile.vertices[0][0] - 30, self.spawn_tile.vertices[0][1]))
        pygame.display.flip()
