import numpy as np

from typing import Optional
from dataclasses import dataclass
import random

from tiles import tiles


@dataclass()
class GridElement:
    """Class that is used to store the state of each element in the TileGrid"""
    tile_id: Optional[int]
    entropy: int = len(tiles)


class TileGrid:
    """Class that is used to preserve the grid state and modify it"""

    def __init__(self, width, height, scaler):
        # Visual
        self.width: int = width
        self.height: int = height
        self.scaler: int = scaler
        self.columns: int = int(height / scaler)
        self.rows: int = int(width / scaler)

        # Grid
        self.size: tuple[int, int] = (self.rows, self.columns)
        self.grid_array: np.ndarray[GridElement] = np.ndarray(shape=self.size, dtype=object)
        for x in range(self.rows):
            for y in range(self.columns):
                self.grid_array[x, y] = GridElement(None)
        """
        #basic_grid_element = GridElement(None)
        #self.grid_array.fill(basic_grid_element)
        # I don't understand it, it could easily break when I try to modify the values, and the code is ugly
        # But for now that's ok
        # I was so right about it not working
        """

    def entropy_of(self, x, y) -> int:
        """Returns the number of tiles that have valid borders with the tile of the 4 bordering grid elements"""

        # First add the existing adjacent edges into a list (using None if the adjacent tile is empty)
        adjacent_edges = []
        if y - 1 < 0 or self.grid_array[x, y - 1].tile_id is None:
            adjacent_edges.append(None)
        else:
            adjacent_edges.append(tiles[self.grid_array[x, y - 1].tile_id].adjacency_rules.South)

        if x + 1 > self.columns or self.grid_array[x + 1, y].tile_id is None:
            adjacent_edges.append(None)
        else:
            adjacent_edges.append(tiles[self.grid_array[x + 1, y].tile_id].adjacency_rules.West)

        if y + 1 > self.rows or self.grid_array[x, y + 1].tile_id is None:
            adjacent_edges.append(None)
        else:
            adjacent_edges.append(tiles[self.grid_array[x, y + 1].tile_id].adjacency_rules.North)

        if x - 1 < 0 or self.grid_array[x - 1, y].tile_id is None:
            adjacent_edges.append(None)
        else:
            adjacent_edges.append(tiles[self.grid_array[x - 1, y].tile_id].adjacency_rules.East)

        # Go through 4 adjacent tiles and create set of possible bordering Tiles
        valid_tiles = []
        for tile in tiles:
            valid_tile = True
            for direction, condition in enumerate(adjacent_edges):
                if condition is None:
                    continue
                if condition != tile.adjacency_rules[direction]:
                    valid_tile = False

            if valid_tile:
                valid_tiles.append(tile)
        return len(valid_tiles)

    def collapse_tile(self):
        """When this function is called on a specific tile a valid tile id is selected and it becomes collapsed"""
        pass

    def iterate(self):
        """Chooses a tile with the lowest entropy, collapses that tile"""
        self.grid_array[self.columns // 2, self.rows // 2].tile_id = 5
        print(self.entropy_of(self.columns // 2, self.rows // 2))
        """
        First Calculate entropy of each tile
    
        min_entropy = None
        for i in range(self.rows):
            for j in range(self.columns):
                if self.grid_array[i, j].tile_id is not None:
                    if min_entropy is None:
                        min_entropy = self.entropy_of(i, j)
                        continue
                    min_entropy = min(min_entropy, self.entropy_of(i, j))
        """

    def update(self, surface, images):
        """This function should render all of the collapsed wavelengths every frame"""
        for x in range(self.rows):
            for y in range(self.columns):
                element: GridElement = self.grid_array[x, y]
                if element.tile_id is None:
                    continue
                x_pos = x * self.scaler
                y_pos = y * self.scaler
                surface.blit(images[element.tile_id], (x_pos, y_pos))
