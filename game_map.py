import math
from typing import List, Tuple, Optional
#from __future__ import annotations
import pygame
import os
from game_overlay import Sidebar
from game_unit import Unit
from game_building import Building


class Tile:
    """Tile on the game map
    === Public Attributes ===
    is_empty:
        If this object represents an empty tile
    vertices:
        Coordinates of all the vertices of the tile
    adjacent_tiles:
        All tiles adjacent to this one
    land_image:
        Sprite of the land on the tile
    selected:
        If this tile is selected
    highlighted:
        If this tile is highlighted
    supported_building:
        Building on this tile
    supported_unit:
        Unit on this tile
    animation_sprites:
        Sprites of the animation playing on the tile
    """

    vertices: List[List[int]]
    #adjacent_tiles: List[Tile]
    land_image: pygame.image
    selected: bool
    highlighted: bool
    supported_building: Optional[Building]
    supported_unit: Optional[Unit]
    #animation_sprites: List[pygame.image]

    def __init__(self, vertices: List[Tuple[int, int]] = None, land_name: str = None, supported_unit: Unit = None,
                 supported_building: Building = None) -> None:
        if vertices is None:
            self.vertices = None
            self.is_empty = True
            self.land_image = None
            self.selected = None
            self.highlighted = None
        else:
            self.is_empty = False
            self.vertices = vertices
            self.land_image = pygame.image.load(os.path.join(os.path.dirname(__file__), 'images\\' + land_name + '.png'))
            self.selected = False
            self.highlighted = False
        self.supported_building = supported_building
        self.adjacent_tiles = []
        self.supported_unit = supported_unit
        self.animation_sprites = None

    def pan(self, movement: Tuple[int, int]) -> None:
        """Update the vertices of a tile after a pan
        """
        for vertex in self.vertices:
            vertex[0] += movement[0]
            vertex[1] += movement[1]


class Grid:
    """A class that contains all tiles in the game map
    === Public Attributes ===
    tiles:
        Array of all the tiles
    columns:
        Number of columns in the grid
    rows:
        Number of rows in the grid
    radius:
        Radius of a hexagon tile
    half_height:
        Half of the height of a hexagon tile
    xoffset:
        Number of pixels the map is shifted in the x direction
    yoffset:
        Number of pixels the map is shifted in the y direction
    selected_tile:
        Tile that is currently selected
    selected_building:
        Building that is currently selected
    selected_unit:
        Unit that is currently selected
    current_tile:
        Tile that is selected or supports the selected building or selected unit
    sidebar:
         Object that stores building information
    spawn_tile:
        Tile where the player spawns
    """

    tiles: List[List[Tile]]
    columns: int
    rows: int
    radius: int
    half_height: int
    xoffset: int
    yoffset: int
    selected_tile: Tile
    selected_building: Building
    selected_unit: Unit
    current_tile: Tile
    sidebar: Sidebar
    spawn_tile: Tile

    def __init__(self, columns: int, rows: int, radius: int, lines: List[List[str]], sidebar: Sidebar) -> None:
        # Create map tiles
        self.columns = columns
        self.rows = rows
        self.radius = radius
        self.half_height = round(math.sqrt(radius ** 2 - (1/2 * radius) ** 2))
        self.tiles = []
        self.buildings = []
        self.xoffset = 0
        self.yoffset = 0
        self.selected_tile = None
        self.selected_building = None
        self.selected_unit = None
        self.current_tile = None
        self.sidebar = sidebar
        for _ in range(self.columns):
            self.tiles.append([])

        # Create tile objects and append them to the correct location in tiles
        index_lines = 0
        for x in range(self.columns):
            shifted_x = int(x * (3 / 2) * radius + 1 / 2 * radius)
            for y in range(self.rows):
                if int(lines[index_lines][0]) == x and int(lines[index_lines][1]) == y:
                    shifted_y = y * 2 * self.half_height
                    if x % 2 == 1:
                        shifted_y += self.half_height
                    point_list = self._get_vertices(shifted_x, shifted_y)
                    if lines[index_lines][3] != 'None':
                        new_unit = Unit(lines[index_lines][3])
                    else:
                        new_unit = None
                    new_tile = Tile(point_list, lines[index_lines][2], new_unit)
                    if lines[index_lines][2] == 'spawn':
                        self.spawn_tile = new_tile
                    self.tiles[x].append(new_tile)
                    if index_lines+1 < len(lines):
                        index_lines += 1
                else:
                    new_tile = Tile()
                    self.tiles[x].append(new_tile)

        # Update all the tile's adjacent tile attribute
        for x in range(self.columns):
            for y in range(self.rows):
                current_tile = self.tiles[x][y]
                if not current_tile.is_empty:
                    if x % 2 == 0:
                        if 0 <= x - 1 < self.columns and 0 <= y - 1 < self.rows:
                            current_tile.adjacent_tiles.append(self.tiles[x-1][y-1])
                        if 0 <= y - 1 < self.rows:
                            current_tile.adjacent_tiles.append(self.tiles[x][y-1])
                        if 0 <= x + 1 < self.columns and 0 <= y - 1 < self.rows:
                            current_tile.adjacent_tiles.append(self.tiles[x+1][y-1])
                        if 0 <= x + 1 < self.columns:
                            current_tile.adjacent_tiles.append(self.tiles[x+1][y])
                        if 0 <= y + 1 < self.rows:
                            current_tile.adjacent_tiles.append(self.tiles[x][y+1])
                        if 0 <= x - 1 < self.columns:
                            current_tile.adjacent_tiles.append(self.tiles[x-1][y])
                    else:
                        if 0 <= x - 1 < self.columns:
                            current_tile.adjacent_tiles.append(self.tiles[x-1][y])
                        if 0 <= y - 1 < self.rows:
                            current_tile.adjacent_tiles.append(self.tiles[x][y-1])
                        if 0 <= x + 1 < self.columns:
                            current_tile.adjacent_tiles.append(self.tiles[x+1][y])
                        if 0 <= x + 1 < self.columns and 0 <= y + 1 < self.rows:
                            current_tile.adjacent_tiles.append(self.tiles[x+1][y+1])
                        if 0 <= y + 1 < self.rows:
                            current_tile.adjacent_tiles.append(self.tiles[x][y+1])
                        if 0 <= x - 1 < self.columns and 0 <= y + 1 < self.rows:
                            current_tile.adjacent_tiles.append(self.tiles[x-1][y+1])

    def _get_vertices(self, x: int, y: int) -> List[Tuple[int, int]]:
        """Uses the coordinates of the top right point of a hexagon to calculate the remaining points
        """
        point_list = [[x, y]]  # top left point
        point_list.append([x + self.radius, y])  # top right point
        point_list.append([int(x + 3 / 2 * self.radius), y + self.half_height])  # rightmost point
        point_list.append([x + self.radius, y + 2 * self.half_height])  # bottom right point
        point_list.append([x, y + 2 * self.half_height])  # bottom left point
        point_list.append([int(x - self.radius / 2), y + self.half_height])  # leftmost point
        return point_list

    def find_mouse_grid_location(self, mouse_position: Tuple[int, int]) -> Tuple[int, int]:
        """Finds the grid coordinates of the mouse
        """
        mousex = mouse_position[0] - self.xoffset
        mousey = mouse_position[1] - self.yoffset
        mouse_grid_x = int(mousex // (3 / 2 * self.radius))
        tile_x = mousex % (3 / 2 * self.radius)
        tile_y = mousey % (2 * self.half_height)
        if mouse_grid_x % 2 == 1 and tile_x < (-self.radius / (2 * self.half_height) * abs(tile_y - self.half_height) + 1 / 2 * self.radius):
            mouse_grid_x -= 1
        elif mouse_grid_x % 2 == 0 and tile_x < (self.radius / (2 * self.half_height) * abs(tile_y - self.half_height)):
            mouse_grid_x -= 1
        if mouse_grid_x % 2 == 0:
            mouse_grid_y = int(mousey // (2 * self.half_height))
        else:
            mouse_grid_y = int((mousey - self.half_height) // (2 * self.half_height))
        return mouse_grid_x, mouse_grid_y

    def pan(self, movement: Tuple[int, int]) -> None:
        """Update the offset caused by a pan for the grid and all tiles"""
        self.xoffset += movement[0]
        self.yoffset += movement[1]
        for sublist in self.tiles:
            for tile in sublist:
                if not tile.is_empty:
                    tile.pan(movement)

    def left_click(self, mouse_grid_location: Tuple[int, int], mouse_sidebar_location: Optional[int], to_build: Optional[str]) -> Optional[str]:
        if mouse_sidebar_location is None:
            clicked_tile = self._find_clicked_tile(mouse_grid_location)
            if to_build is None:
                self.handle_select(clicked_tile)
            else:
                self.handle_build(clicked_tile, to_build)
            return None
        else:
            self.unselect()
            return self.sidebar.building_info[mouse_sidebar_location][0]

    def right_click(self, mouse_grid_location: Tuple[int, int], action_type: str) -> None:
        pass

    def handle_select(self, clicked_tile: Tile) -> None:
        if clicked_tile is not None:
            if self.selected_tile == clicked_tile:
                self.unselect()
            elif self.selected_unit is not None and clicked_tile.highlighted and \
                    self.selected_unit != clicked_tile.supported_unit:
                # Moves selected unit to clicked highlighted tile
                for tile in self.current_tile.adjacent_tiles:
                    if not tile.is_empty:
                        tile.highlighted = False
                clicked_tile.supported_unit = self.selected_unit
                self.current_tile.supported_unit = None
                self.current_tile = clicked_tile
                self.highlight(clicked_tile)
            elif (self.selected_building is not None and self.selected_building == clicked_tile.supported_building) or \
                    (self.selected_unit is not None and self.selected_unit == clicked_tile.supported_unit):
                # Selects tile underneath building or unit
                self.unselect()
                self.select_tile(clicked_tile)
                self.current_tile = clicked_tile
            else:
                self.unselect()
                if clicked_tile.supported_unit is not None:
                    self.select_unit(clicked_tile, clicked_tile.supported_unit)
                    self.current_tile = clicked_tile
                elif clicked_tile.supported_building is not None:
                    self.select_building(clicked_tile.supported_building)
                    self.current_tile = clicked_tile
                else:
                    self.select_tile(clicked_tile)
                    self.current_tile = clicked_tile

    def select_tile(self, clicked_tile: Tile) -> None:
        self.selected_tile = clicked_tile
        self.selected_tile.selected = True

    def select_building(self, supported_building: Building) -> None:
        self.selected_building = supported_building
        self.selected_building.selected = True

    def select_unit(self, clicked_tile: Tile, supported_unit: Unit) -> None:
        self.selected_unit = supported_unit
        self.selected_unit.selected = True
        self.highlight(clicked_tile)

    def highlight(self, clicked_tile: Tile) -> None:
        for tile in clicked_tile.adjacent_tiles:
            if not tile.is_empty and tile.supported_unit is None and tile.supported_building is None:
                tile.highlighted = True

    def handle_build(self, clicked_tile: Tile, to_build: str) -> None:
        if clicked_tile is not None:
            if clicked_tile.supported_building is None and clicked_tile.supported_unit is None:
                new_building = Building(to_build)
                self.buildings.append(new_building)
                clicked_tile.supported_building = new_building

    def unselect(self) -> None:
        if self.selected_tile is not None:
            self.selected_tile.selected = False
            self.selected_tile = None
        elif self.selected_building is not None:
            self.selected_building.selected = False
            self.selected_building = None
        elif self.selected_unit is not None:
            self.selected_unit.selected = False
            self.selected_unit = None
            for tile in self.current_tile.adjacent_tiles:
                if not tile.is_empty:
                    tile.highlighted = False
        self.current_tile = None

    def _find_clicked_tile(self, mouse_grid_location: Tuple[int, int]) -> Optional[Tile]:
        if 0 <= mouse_grid_location[0] < self.columns and 0 <= mouse_grid_location[1] < self.rows:
            clicked_tile = self.tiles[mouse_grid_location[0]][mouse_grid_location[1]]
            if not clicked_tile.is_empty:
                return clicked_tile
        return None

    def set_spawn_building(self) -> None:
        new_building = Building('spawn_tower')
        self.spawn_tile.supported_building = new_building

